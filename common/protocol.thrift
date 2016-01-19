
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
 * Response of a getMessages query.
 */
struct GetMessagesResponse {
	/** New messages per chat. */
	1: list<ChatData> chatData,
}

/**
 * Response of a getUserPublicKey query.
 */
struct GetUserPublicKeyResponse {
	/** The public key of the target user. */
	1: string publicKey
}

/**
 * Different attribute types used in contact lists.
 */
enum ContactAttributeType {
	ALIAS
}

/**
 * Encapsulates one contact.
 */
struct Contact {
	/** Username of the contact. */
	1: string username,
	/** Extandable set of user attributes */
	2: map<ContactAttributeType, string> attributes,
}

/**
 * The different types of updates.
 */
enum ContactUpdateType {
	CREATED,
	UPDATED,
	DELETED,
}

/**
 * Encapsulates an update.
 */
struct ContactUpdate {
	/** The contact itself */
	1: Contact contact,
	/** Type of what has been done. */
	2: ContactUpdateType updateType,
}

/**
 * Response of a getContactListResponse.
 */
struct GetContactListResponse {
	/** Version counter at this time. */
	1: i32 version,
	/** List of contacts the user has. */
	2: list<ContactUpdate> contactUpdates
}

/**
 * Reponse of a addToContactList query
 */
struct AddToContactListResponse {
	/** The new version after the update */
	1: i32 version,
}

/**
 * Reponse of a removeFromContactList query
 */
struct RemoveFromContactListResponse {
	/** The new version after the update */
	1: i32 version,
}

/**
 * Response of a updateContactList query.
 */
struct UpdateContactListReponse {
	/** The new version after the update */
	1: i32 version,
}

/**
 * Response of a getPrivateKeys query.
 */
struct GetPrivateKeysResponse {
	/** The cryptographic key pair used for login and encryption. */
	1: EncryptedKeyPair userKeyPair,
	/** The cryptographic key pair used to exchange keys. */
	2: EncryptedKeyPair exchangeKeyPair
}

/**
 * Response of a requestLoginChallenge.
 */
struct RequestLoginChallengeResponse {
	/** The challenge. */
	1: string challenge
}

/**
 * Communication interface between catmail server und catmail clients.
 */
service CatMailService {

	/**
	 * Requests the encrypted private keys to sign a login challenge.
	 */
	GetPrivateKeysResponse getPrivateKeys(
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
	 * Returns a login challenge from the server.
	 */
	RequestLoginChallengeResponse requestLoginChallenge(
		/** The name of the user. */
		1: string username,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
	),
	
	/**
	 * Logs the user in
	 */
	LoginResponse login(
		/** The name of the user. */
		1: string username,
		/** Challenge received from the server */
		2: string challenge,
		/** Signed string "challenge/hostname" */
		3: string signature,
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
		/** The chat where to send the message to. */
		3: i64 chatId,
		/** The message itsself. */
		4: string message,
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
	GetMessagesResponse getMessages(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** Chats where to fetch messages. An empty list queries all chats. */
		3: list<Chat> chats,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that there is no chat with this id. */
		3: ChatDoesNotExistException chatDoesNotExistException,
	),
	
	/**
	 * Marks message with given MessageID and older as read.
	 */
	 void markMessagesAsRead(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
	 	/** The chat which contains the messages. */
	 	3: i64 chatId,
	 	/** The newest MessageID. */
	 	4: i64 messageId, 
	 ) throws (
	 	/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** chat dosen't exist. */
		2: ChatDoesNotExistException chatDoesNotExistException,
		/** Message doesn't exist. */
		3: MessageDoesNotExistException messageDoesNotExistException
		/** Combination of username and password is wrong. */
		4: InvalidSessionException invalidSessionException,
	),

	/**
	 * Downloads the public key of any user
	 */
	GetUserPublicKeyResponse getUserPublicKeyResponse(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** Get the public key of this user */
		3: string targetUser,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that the target user does not exist. */
		3: UserDoesNotExistException userDoesNotExistException,
	),

	/**
	 * Queries an incremental update a user's contact list.
	 *
	 * The specified version indicates the latest version that has been queried
	 * previously. If version is 0, the full contact list will be returned with
	 * all incremental changes applied.
	 * If the given version is larger than 0, the update will be incremental.
	 */
	GetContactListResponse getContactList(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** Verion number the client has */
		3: i32 version,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
	),

	/**
	 * Adds an entry to the contact list. Increments the version counter to inform other clients.
	 */
	AddToContactListResponse addToContactList(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** The name of the user who will be added */
		3: string userToAdd,
		/** Additional information to store. */
		4: map<ContactAttributeType, string> attributes,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that the target user does not exist. */
		3: UserDoesNotExistException userDoesNotExistException,
	),

	/**
	 * Updates an entry of the contact list. Increments the version counter to inform other clients.
	 */
	UpdateContactListReponse updateContactList(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** The name of the user who will be updated */
		3: string userToUpdate,
		/** Additional information to update. */
		4: map<ContactAttributeType, string> attributes,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that the target user does not exist. */
		3: UserDoesNotExistException userDoesNotExistException,
	),

	/**
	 * Adds an entry to the contact list. Increments the version counter to inform other clients.
	 */
	RemoveFromContactListResponse removeFromContactList(
		/** The name of the user. */
		1: string username,
		/** The user's session token. */
		2: string sessionToken,
		/** The name of the user who will be deleted */
		3: string userToDelete,
	) throws (
		/** Something went dramatically wrong. */
		1: InternalException internalException,
		/** Combination of username and password is wrong. */
		2: InvalidSessionException invalidSessionException,
		/** Indicates that the target user does not exist. */
		3: UserDoesNotExistException userDoesNotExistException,
	),

}
