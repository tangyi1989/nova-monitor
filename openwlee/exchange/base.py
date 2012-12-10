
class Reporter():
    """ Reporter worked in wlee agent to send message to receiver 
    which in wlee daemon. """
    def __init__(self, *args, **kargs):
        pass
    
    def report(self, data):
        """ Block or not, guarantee or not, that's a question."""
        raise NotImplementedError
    
class Receiver():
    """ A receiver worked in wlee daemon to receive from wlee agent. 
     """
    def __init__(self, *args, **kargs):
        pass
    
    def receive(self):
        """ A block method would blocking until it receive a message """
        raise NotImplementedError