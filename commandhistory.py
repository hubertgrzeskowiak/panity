class Step(object):
	"""Interface to the objects expected in CommandHistory."""
	def undo(self):
		pass
	def do(self):
		pass


class CommandHistory(object):
	def __init__(self):
		self.undoable = []
		self.redoable = []

	def undo(self):
		try:
			step = self.undoable.pop()
		except IndexError:
			pass
		else:
			step.undo()
			self.redoable.append(step)

	def redo(self):
		try:
			step = self.redoable.pop()
		except IndexError:
			pass
		else:
			step.do()

	def addStep(self, step):
		"""Add a step that has been just performed.
		A "step" needs to have a do() method (think of as redo) and undo().
		This method resets the list of redoable commands.
		"""
		self.undoable.append(step)
		self.redoable.clear()
		print step

	def canUndo(self):
		return self.undoable != []

	def canRedo(self):
		return self.redoable != []