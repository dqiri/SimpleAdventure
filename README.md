# SimpleAdventure
A Simple Python choose your own adventure player that can read a script and play it.

##Scriptformat
`<event label>;<content>;<choice label>|<choice description>;<choice label>|<choice description;...`

##Example
`start;Today is the start of the day;noon|Go to Noon;night|Sleep Until Night;somethingelse;Something Else`
`noon;You are now at noon;start|Restart?`
etc etc
