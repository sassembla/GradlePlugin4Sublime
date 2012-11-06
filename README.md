# Gradle plugin for Sublime Text 2

This is a plugin for the [Sublime Text 2](http://www.sublimetext.com/) text editor.   
Input gradle-command to your "build.gradle" through Sublime Text 2.


## Prerequisite
Please check below:  
* Gradle is installed and enable. See [Gradle.org](http://gradle.org/)


## Installation
From shell/Terminal (on OS X, Linux or Cygwin), via git:  

    cd ~/"Library/Application Support/Sublime Text 2/Packages/" 
    # location on OS X; will be different on Linux & Windows
    
    git clone https://github.com/sassembla/GradlePlugin4Sublime.git
    
The plugin should be picked up automatically. If not, restart Sublime Text.


## Usage
* Open "gradlie-ruled" folder which includes "build.gradle" with Sublime Text 2.
* Open the file what you want to edit.
* Then open Command Palette > type some command for gradle.. > hit enter.

e.g. "build"
    
	Command Palette > type "gradle build" > gradle will start building project.

You can see the progress of Gradle-command through Sublime's console.

	^ + ` > see progress of Gradle-command.

## Other utility(experimental)
There are some utilities not included in Gradle.

	Command Palette > type "GradleUtil open Test Report" >   
	  plugin will open the result of the tests of current project.(if exist!)
	
This is applied for Mac OS X yet.



## For multiple "build.gradle"
If there is mulitple "build.gradle" settings in that project,   
this plugin will use the "build.gradle" that located the top of that 
project's folder hierarchy.  

When you wanna use specify "build.gradle" located at not toplevel of the folder,   
open the specific folder that includes the "build.gradle" you want to use.



## Settings
This plugin strongly depends on Gradle.  
You can customize the path of gradle.bin via below,

`Preferences > Package Settings > Gradle > Settings - Default (or Settings - User)`



## Bugs and Feature Requests

<https://github.com/sassembla/GradlePlugin4Sublime/issues>


## License

MIT License
