
namespace java de.catmail.api
namespace cpp  catmail.api

exception InternalException {
	
}

exception InvalidLoginCredentialsException {
	
}

exception InvalidSessionException {
	
}

exception UserAlreadyExistsException {
	
}

exception UserDoesNotExistException {
	1: string username
}

exception ChatDoesNotExistException {
	
}

exception MessageDoesNotExistException {

}

exception InvalidMessageException {
	
}

/**
 * Holds a keypair.
 */
struct EncryptedKeyPair {
	/** The encrypted secret key. */
	1: string encryptedSecretKey,
	/** The nonce. */
	2: string nonce,
	/** The public key. */
	3: string publicKey
}

/**
 * Response of a login query.
 */
struct LoginResponse {
	/** The user's session token. */
	1: string sessionToken,
	/** The cryptographic key pair used for login and encryption. */
	2: EncryptedKeyPair userKeyPair,
	/** The cryptographic key pair used to exchange keys. */
	3: EncryptedKeyPair exchangeKeyPair
}

/**
 * Reponse of a createChat query.
 */
struct CreateChatResponse {
	/** The id of the newly created chat. */
	1: i64 chatId,
}

/**
 * Encapsulated information to add an existing user to a chat.
 */
struct AddChatUser {
	/** Name of the user to add. */
	1: string username,
	/** The encrypted key (user individual) to read the messages in the chat. */
	2: string key,
}

/**
 * Response of a sendMessage query.
 */
struct SendMessageResponse {
	/** Updated current chat version. */
	1: i64 messageId,
}

/**
 * Encapsulates some chat data.
 */
struct Chat {
	/** Id of the chat. */
	1: i64 chatId,
	/** Current messageId the client has. */
	2: i64 messageId,
}

/**
 * Meta data and messages list of a chat room.
 */
struct ChatData {
	/** The chat meta data. */
	1: Chat chat,
	/** Ordered list of messages. */
	2: list<string> messages
}

/**
 * Response of a getNewMessages query.
 */
struct GetNewMessagesResponse {
	/** New messages per chat. */
	1: list<ChatData> chatData,
}

/**
 * Communication interface between catmail server und catmail clients.
 */
service CatMailService {
	
	/**
	 * Logs the user in
	 */
	LoginResponse login(
		/** The name of the user. */
		1: string username,
		/** The password of the user. */
		2: string password
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidLoginCredentialsException invalidLoginCredentialsException
	),

	/**
	 * Logs the user out.
	 */
	void logout(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException
	),

	/**
	 * Creates a new user. As there is an open user registration, every new user can call this method by himself.
	 */
	void createUser(
		/** The new username. */
		1: string username,
		/** The password. */
		2: string password,
		/** The cryptographic key pair used for login and encryption. */
		3: EncryptedKeyPair userKeyPair,
		/** The cryptographic key pair used to exchange keys. */
		4: EncryptedKeyPair exchangeKeyPair
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Indicates that there is already a user with this username. */
		2: UserAlreadyExistsException userAlreadyExistsException
	),

	/**
	 * Deletes the current user.
	 */
	void deleteUser(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException
	),

	/**
	 * Creates a new chat.
	 */
	CreateChatResponse createChat(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** Add these users to the new chat. */
		3: list<AddChatUser> usersToAdd,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that one or more users does not exist */
		3: UserDoesNotExistException userDoesNotExistException,
	),

	void addToChat(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** The id of the chat. */
		3: i64 chatId,
		/** Add these users to the new chat. */
		4: list<AddChatUser> usersToAdd,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that there is no chat with this id. */
		3: ChatDoesNotExistException chatDoesNotExistException,
		/** Indicates that one or more users does not exist */
		4: UserDoesNotExistException userDoesNotExistException,
	)

	/**
	 * The user leaves an existing chat.
	 */
	void leaveChat(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** The id of the chat to delete. */
		3: i64 chatId,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that there is no chat with this id. */
		3: ChatDoesNotExistException chatDoesNotExistException
	),

	/**
	 * Deletes an existing chat.
	 */
	void deleteChat(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** The id of the chat to delete. */
		3: i64 chatId,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that there is no chat with this id. */
		3: ChatDoesNotExistException chatDoesNotExistException
	),

	/**
	 * Sends a message to a specific chat.
	 */
	SendMessageResponse sendMessage(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** The message itsself. */
		3: string message,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that there is no chat with this id. */
		3: ChatDoesNotExistException chatDoesNotExistException,
		/** Indicates that the message content is invalid (e.g. to long) */
		4: InvalidMessageException invalidMessageException
	),

	/**
	 * Fetches all new messages from server.
	 */
	GetNewMessagesResponse getNewMessages(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** Chats where to fetch messages. */
		3: list<Chat> chats,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that there is no chat with this id. */
		3: ChatDoesNotExistException chatDoesNotExistException,
	)
	
	/**
	 * Marks message with given MessageID and older as read.
	 */
	 void markMessagesAsRead(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
	 	/**The chat which contains the messages. */
	 	3: i64 chatID,
	 	/**The newest MessageID. */
	 	4: i64 MessageID, 
	 ) throws (
	 	/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** chat dosen't exist. */
		2: ChatDoesNotExistException chatDoesNotExistException,
		/** Message doesn't exist. */
		3: MessageDoesNotExistException messageDoesNotExistException
		/** Combination of username and password is wrong. */
		4: InvalidSessionException invalidSessionException,
	)

}
