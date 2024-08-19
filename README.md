# Sit, Boy!

## Running the Game Without SQL Backend
In main.py, comment out every line referencing the sqlEventHandler object.

pyjsdl-ts courtesy of **jggatc**
- github repo: https://github.com/jggatc/pyjsdl-ts
- website: https://gatc.ca/projects/pyjsdl-ts/

To run the game, you will need to install pygame: https://www.pygame.org/wiki/GettingStarted

Currently working out transcrypt compilation bugs. Ideally, once those are done, navigate to the directory and type the command:

```transcrypt -n main.py```

## Planning Sheet

### Game Dev Plan
- needs backend. python to mysql backend.
	- testdb in mysql server community version localhost server (for now)
- start menu with name of game and play or quit button
- tutorial explaining what the game's about?
- the game:
	- a dog is standing there, hanging out.
	- you tell the dog to sit
	- the dog sits after a random time
	- you press the 'reward' button
		- time it takes between sit and reward is recorded and sent to db
	- at end of game, show their score

### elements of the program
3 parts to every game:
1. window
2. game loop
3. event handler

the big parts of this game:
1. sprite animations
	- stand, lick, sit, walk, run
2. random time pass
	- a random double value translated to seconds - 1-5 seconds
3. menu
4. user interactions
	- click buttons
	- command sit
	- give reward

### organizing the code
- sprite sheet
- sprite animation
- main
	- event handler
	- game loop
	- window

### features left to implement
- [ ] dynamic window for different user screens
	- [ ] mobile
	- [ ] desktop
	- [ ] tablet
- [ ] db connection
	- [x] animation update insert event
	- [x] user input update insert event
	- [ ] demographics data collection
- [ ] user reward system
	- [ ] basic instructions in the game loop: when the dog sits down completely, press the enter/return key to reward them.
- [ ] game instructions page
	- [ ] potential instruction locations:
		- [ ] on start menu
		- [ ] behind a menu button to access instructions
		- [ ] behind a game button to access instructions (pauses game while this happens)