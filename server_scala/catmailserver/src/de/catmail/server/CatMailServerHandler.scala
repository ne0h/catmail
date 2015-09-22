package de.catmail.server

import de.catmail.api.AddChatUser
import de.catmail.api.CatMailService
import de.catmail.api.Chat
import de.catmail.api.CreateChatResponse
import de.catmail.api.EncryptedKeyPair
import de.catmail.api.GetNewMessagesResponse
import de.catmail.api.LoginResponse
import de.catmail.api.SendMessageResponse

/**
 * @author ne0h
 */
class CatMailServerHandler extends CatMailService.Iface {
	
	override def login(username: String, password: String): LoginResponse = {
		println("username: " + username)
		
		return new LoginResponse(username, null, null)
	}
	
	override def logout(username: String, sessionToken: String) {
		
	}
	
	override def createUser(username: String, password: String, userKeyPair: EncryptedKeyPair,
			exchangeKeyPair: EncryptedKeyPair) {
		
	}
	
	override def deleteUser(username: String, password: String) {
		
	}
	
	override def createChat(username: String, sessionToken: String,
			usersToAdd: java.util.List[AddChatUser]): CreateChatResponse = {
		
		return new CreateChatResponse()
	}
	
	override def addToChat(username: String, sessionToken: String, chatId: Long,
			usersToAdd: java.util.List[AddChatUser]) {
		
	}
	
	override def leaveChat(username: String, sessionToken: String, chatId: Long) {
		
	}
	
	override def deleteChat(username: String, sessionToken: String, chatId: Long) {
		
	}
	
	override def sendMessage(username: String, sessionToken: String, chatId: Long,
			message: String): SendMessageResponse = {
		
		return new SendMessageResponse()
	}
	
	override def getNewMessages(username: String, sessionToken: String,
			chats: java.util.List[Chat]): GetNewMessagesResponse = {
	
		return new GetNewMessagesResponse()
	}
	
	override def markMessagesAsRead(username: String, sessionToken: String, chatId: Long, messageId: Long) {
		
	}
	
}