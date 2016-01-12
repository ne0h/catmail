from contact import CatMailContact
from lib.rwlock import RWLock

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
		if not contactListResponse is None and not contactListResponse.contacts is None:
			for c in contactListResponse.contacts:
				self._atomic_list.append(
						CatMailContact(
								c.username,
								"" #TODO alias, other attributes...
							)
					)
		self._release_write_lock()

	def __init__(self):
		super(ContactList, self).__init__()
		self.__revision = 0

class ConversationsList(AtomicList):
	def get_conversations_iterator(self):
		return self._get_iterator()

	def update_conversations():
		self._acquire_write_lock()
		self._release_write_lock()

	def __init__(self):
		super(ConversationsList, self).__init__()
