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
