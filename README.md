# PresentationJSON

A terminal server/UI server for Posix systems[^posix].

## Theory of operation

### Command Pipeline
The presentation server ("server") listens to a named pipe named `presentation_json.cmd` in the `/tmp/pjpipelines` 
directory.  If the directory does not exist, the application will attempt to create it.  The command pipe is created by
the server, but won't object if it already exists.

Clients send commands to create sessions, delete sessions, send data to a session, or to close the server itself. All
communication on the command pipeline is in utf-8 plain text, and the core commands are limited to the printable ascii
subset.  All commands are case-sensitive and begin with the `@` (Aka the "at sign", "commercial at", "snabel-a", 
"Klammerraffe", etc.), and use it as a delimiter as well: 

| Command           | Description                                              |
|-------------------|----------------------------------------------------------|
| `@QUIT@`          | Terminate the server.  May not be retained in the future |
| `@TERM@{name}`    | Create a terminal session named `{name}`                 |
| `@JSON@{name}`    | Create a presentation session named `{name}`             |
| `@KILL@{name}`    | Create a presentation session named `{name}`             |
| `@{name}@{data}`  | Sends `{data}` to session named `{name}`                 |

All other traffic will be ignored, and no errors will be reported unless a response pipe has been established. Since a 
response pipe isn't created until *after* session creation is successful, if a session name already exists, or there is
some other kind of error, it can't be reported back to the sender.  Care should be taken to use unique session names.

Return pipes are created in the same directory as the command pipeline, and have the same name as the session name.  
The server will attempt to delete them when it closes, but will reuse them if they already exist


### Terminal Server

Unless otherwise specified, terminals are 80 columns by 25 rows, do not automatically echo keystrokes sent to them, and
supports the VT100/[ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code)  Escape Codes, with some support for the 
VT220, VT520, and `TERM=linux` — Escape code support comes via the [pyte](https://github.com/selectel/pyte) project.

#### TODO

- [ ] Support scrollback
- [ ] Mouse actions for cut/copy/paste

### Presentation System
The presentation system (you know the primary purpose of this project), has not been designed yet.

#### TODO
- [ ] Design it
- [ ] Implement it
 
### Technical Limitations

#### Pipes
Because of the default behavior of pipes, the app will halt when waiting for pipes to be opened on both sides of the
pipeline.  The app attempts to mitigate this somewhat, and will do more in the future, but well-behaved clients should:

1. Open the command pipe as soon as possible in their startup
2. Open their return pipe immediately after requesting a new session.

These steps will ensure the best performance of the server and client

## Footnotes:

[^posix] No attempt as been made to test if it will work on Windows, and no code has been written to facilitate it.
It may be added in the future