What I learned in my 1st time using a Shell and Ubuntu (In-general)
What 755 means?
Basically this is the permission encoded value, three digits are for the ff: users, groups, and others. Its value
comes from r (read) = 4, w (write) = 2, and x (execute) = 1. Meaning, 7 means that user can read, write, and execute.
While 5 means that group (2nd digit) can read and execute, but cannot write.

What chown does?
Changes the ownership of a file or directory, formatted as this: sudo chown users:groups "file/directory"

What r/w/x mean on a directory?
See my answer for "What 755 means? above

The difference between a user and group?
A user has certain permissions and things they can do individually, however, a group consists of a number of users
who share the same permission/access. Which is really great for like a group of people with certain levels of
access/power to a project for example.

What sudo does?
sudo, or superuser do is something you attach before a command to ran it as root (admin), in instances where you're 
not permitted to do something (like accessing a directory or a ranning a command). Basically, it bypasses that by
giving you root privileges.	
