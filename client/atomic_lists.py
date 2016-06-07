from contact import CatMailContact
from lib.rwlock import RWLock
from enum import Enum

class AtomicList:
	def _acquire_write_lock(self):
		self.__rwlock.acquire_write()

	def _release_write_lock(self):
		self.__rwlock.release()

	def acquire_read_lock(self):
		self.__rwlock.acquire_read()

	def release_read_lock(self):
		self.__rwlock.release()

	"""This returns a python iterator to loop over the contacts.

	.. note:: The iterator can not be recycled!
	"""
	def _get_iterator(self):
		#generator for iterator
		self.acquire_read_lock()
		for c in self._atomic_list:
			yield c
		self.release_read_lock()

	def _clear_list(self):
		self.__atomic_list = []

	def __init__(self):
		self.__rwlock = RWLock()
		self._atomic_list = []

class ContactList(AtomicList):
	class UPDATE_TYPES(Enum):
		CREATED = 0
		UPDATED = 1
		DELETED = 2

	def get_contacts_iterator(self):
		return self._get_iterator()

	def get_contact_list_revision(self):
		rv = 0
		self.acquire_read_lock()
		rv = self.__revision
		self.release_read_lock()
		return rv

	def update_contacts(self, contactListResponse):
		self._acquire_write_lock()
		self._atomic_list = []
		def delete(contact):
			print("Deleting contact: %s" % contact.username)
			i = 0
			for i, c in self._atomic_list:
				if c.getContactID() == contact.username:
					break
			self._atomic_list.pop(i)
		def add(contact):
			print("Adding contact: %s" % contact.username)
			self._atomic_list.append(
				CatMailContact(
						contact.username,
						"" #TODO alias, other attributes...
					)
				)

		if not contactListResponse is None \
				and not contactListResponse.contactUpdates is None \
		:
			print("updating contacts")	
			for update in contactListResponse.contactUpdates:
				updateType = self.UPDATE_TYPES(update.updateType)
				if updateType == self.UPDATE_TYPES.CREATED:
					add(update.contact)
				elif updateType == self.UPDATE_TYPES.UPDATED:
					# since order does not matter:
					# simply delete old instance, add new update
					delete(update.contact)
					add(update.contact)
				elif updateType == self.UPDATE_TYPES.DELETED:
					delete(update.contact)
				else:
					raise RuntimeError("Received invalid update type: %s" % \
							str(update.updateType))
			self.__revision = contactListResponse.version
		self._release_write_lock()

	def __init__(self):
		super(ContactList, self).__init__()
		self.__revision = 0

class ConversationsList(AtomicList):
	def get_conversations_iterator(self):
		return self._get_iterator()

	def update_conversations(self):
		self._acquire_write_lock()
		self._release_write_lock()

	def get_conversations_with_contact_id(self, cid, private_only=False):
		conversationIDs = []
		for conversation in self.get_conversations_iterator():
			if conversation.getConversationID() == cid \
					and (private_only and conversation.is_private()) \
					or not private_only:
				conversationIDs.append(cid)
		return conversationIDs

	def __init__(self):
		super(ConversationsList, self).__init__()
