#!/usr/bin/python

from ansible.module_utils.basic import *
from subprocess import check_output, CalledProcessError

_argument_spec = \
{ "check": { "required":False, "type":"list" }
, "set":   { "required":True, "type":"list" }
, "fatal": { "required":False, "type":"bool", "default":True }
}

def main():
	"""
	Are we in state X?
	If not, make it so and check again.
	With shell commands.

	Note:	This is engineering in the real world, so state can only be defined empirically.
		Or so physicists will tell you.
		And for once they are right.
		And just because an installer says that it succeeded doesn't mean that it did.
		So we check and check and check again.

	Arguments:
		check:	A list of commands to execute.  If any return a non-zero code, the check fails.
		set:	A list of commands.  If any fail, execution will stop.

	Example:
		- name: a fish called wanda
		  bashops:
		    check:
		    - ["/usr/bin/test", "-e", "wanda"]
		    set:
		    - ["/usr/bin/touch", ",wanda"]
		    - ["/bin/mv", ",wanda", "wanda"]
	"""
	module = AnsibleModule(argument_spec=_argument_spec)

	name = module.params.get("name", "Thing")
	if "check" in module.params:
		code, stdout = _exec(module.params["check"])
		if code == 0:
			"""
			We are already in the prescribed state?  Great!  Nothing to do.
			"""
			changed = False
			print(":-) %s is already perfect." % name)
		else:
			"""
			Uh oh, there is work to do.
			"""
			changed = True
			print(":-O Setting %s..." % module.params.get("name", "Thing"))
			code, stdout = _exec(module.params["set"])
			_failure_may_be_fatal(code, module)
			# Checking that the set succeeded:
			code, stdout = _exec(module.params["check"])
			_failure_may_be_fatal(code, module)
			print(":-) Completed %s" % module.params.get("name", "Thing"))
	else:
		"""
		No check? OK, then just set the state to the prescribed value.
		"""
		changed = True
		code, stdout = _exec(module.params["set"], fatal=failure_is_fatal)
		_failure_may_be_fatal(code, module)
		
	response = {"exit_code": 0, "stdout":"", "stderr":""}
	module.exit_json(changed=False, meta=response)

def _failure_may_be_fatal(code, module):
	if (code != 0):
		name = module.params.get("name", "Thing")
		print("X-( %s returned non-zero." % name)
		failure_is_fatal = module.params["fatal"]
		if failure_is_fatal:
			raise Exception("Non-zero exit code.")

def _exec(commands, fatal=True, name="Thing"):
	print("commands:", commands)
	try:
		code = 0
        	for command in commands:
			print("command:", command)
			stdout = subprocess.check_output(command)
	except CalledProcessError as e:
		stdout = e.output
		code = e.returncode
	return (code, stdout)


if __name__ == '__main__':  
	main()
