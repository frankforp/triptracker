# Util/Observer.py
# Class support for "observer" pattern.
import threading


class Observer:
    def update(self, observable, arg):
        '''Called when the observed object is
        modified. You call an Observable object's
        notifyObservers method to notify all the
        object's observers of the change.'''
        pass


class Observable:
    def __init__(self):
        self.obs = []
        self.changed = 0
        self.mutex = threading.RLock()

    def addObserver(self, observer):
        try:
            self.mutex.acquire();
            if observer not in self.obs:
                self.obs.append(observer)
        finally:
            self.mutex.release()

    def deleteObserver(self, observer):
        try:
            self.mutex.acquire()
            self.obs.remove(observer)
        finally:
            self.mutex.release()

    def notifyObservers(self, arg=None):
        '''If 'changed' indicates that this object
        has changed, notify all its observers, then
        call clearChanged(). Each observer has its
        update() called with two arguments: this
        observable object and the generic 'arg'.'''

        self.mutex.acquire()
        try:
            if not self.changed: return
            # Make a local copy in case of synchronous
            # additions of observers:
            localArray = self.obs[:]
            self.clearChanged()
        finally:
            self.mutex.release()
        # Updating is not required to be synchronized:
        for observer in localArray:
            observer.update(self, arg)

    def deleteObservers(self):
        try:
            self.mutex.acquire()
            self.obs = []
        finally:
            self.mutex.release()

    def setChanged(self):
        try:
            self.mutex.acquire()
            self.changed = 1
        finally:
            self.mutex.release()

    def clearChanged(self):
        try:
            self.mutex.acquire()
            self.changed = 0
        finally:
            self.mutex.release()

    def hasChanged(self):
        try:
            self.mutex.acquire()
            return self.changed
        finally:
            self.mutex.release()

    def countObservers(self):
        try:
            self.mutex.acquire()
            return len(self.obs)
        finally:
            self.mutex.release()
