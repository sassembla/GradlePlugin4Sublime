# Gradle plugin for Sublime Text 2 v1.0

This is a plugin for the [Sublime Text 2](http://www.sublimetext.com/) text editor.   
Input gradle-command to your "build.gradle" through Sublime Text 2.


## Prerequisite
Please check below:  
* Gradle should be installed and enabled. Visit [Gradle.org](http://gradle.org/)


## Installation
From shell/Terminal (on OS X, Linux or Cygwin), via git:  

    cd ~/"Library/Application Support/Sublime Text 2/Packages/" 
    # location on OS X; will be different on Linux & Windows
    
    git clone https://github.com/sassembla/GradlePlugin4Sublime.git
    
The plugin should be picked up automatically. If not, restart Sublime Text.

**! Please set your gradle/gradle.bat path first. see [Settings](#settings) !**

## Usage
* Open "gradlie-ruled" folder which includes "build.gradle" with Sublime Text 2.
* Open the file what you want to edit.
* Then open Command Palette > type some command for gradle.. > hit enter.

e.g. "build"
    
	Command Palette > type "gradle build" > gradle will start building project.

You can see the progress of Gradle-command through Sublime's console.

	^ + ` > see progress of Gradle-command.

## Supported Gradle commands
These commands are supported. Default setting as [ apply plugin:"java" ]

	assemble	
	build
	buildDependents
	buildNeeded
	classes
	clean
	jar
	testClasses
	javadoc	
	dependencies	
	help
	projects	
	properties
	tasks	
	check
	test

and there are some plugin utilities.  

	manual input  
	which gradle  
	open Test Report(experimental, only for Mac OS X.)  





## For multiple "build.gradle"
If there is mulitple "build.gradle" settings in that project,   
this plugin will use the "build.gradle" that located the top of that 
project's folder hierarchy.  

When you wanna use specify "build.gradle" located at not toplevel of the folder,   
open the specific folder that includes the "build.gradle" you want to use.



## Settings
This plugin strongly depends on Gradle.  
You should customize the path of gradle/gradle.bat via below,

`Preferences > Package Settings > Gradle > Settings - Default (or Settings - User)`



## Bugs and Feature Requests

<https://github.com/sassembla/GradlePlugin4Sublime/issues>


## License

MIT License
