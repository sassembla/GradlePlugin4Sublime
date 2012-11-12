# coding=UTF-8

import sublime
import sublime_plugin
from functools import partial
from Gradle import BuildThread, ThreadProgressObserver, Gradle

class Gassemble(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('assemble')
    RunCommand.runCommand(self.view, command)


class Gbuild(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('build')
    RunCommand.runCommand(self.view, command)


class Gbuilddependents(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('buildDependents')
    RunCommand.runCommand(self.view, command)


class Gbuildneeded(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('buildNeeded')
    RunCommand.runCommand(self.view, command)


class Gcheck(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('check')
    RunCommand.runCommand(self.view, command)


class Gclasses(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('classes')
    RunCommand.runCommand(self.view, command)


class Gclean(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('clean')
    RunCommand.runCommand(self.view, command)


class Gdependencies(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('dependencies')
    RunCommand.runCommand(self.view, command)


class Ghelp(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('help')
    RunCommand.runCommand(self.view, command)


class Gjar(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('jar')
    RunCommand.runCommand(self.view, command)


class Gjavadoc(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('javadoc')
    RunCommand.runCommand(self.view, command)


class Gprojects(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('projects')
    RunCommand.runCommand(self.view, command)


class Gproperties(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('properties')
    RunCommand.runCommand(self.view, command)


class Gtasks(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('tasks')
    RunCommand.runCommand(self.view, command)


class Gtest(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('test')
    RunCommand.runCommand(self.view, command)


class Gtestclasses(sublime_plugin.TextCommand):
  def run (self, edit) :
    command = sublime.load_settings("Gradle.sublime-settings").get("command").get('testClasses')
    RunCommand.runCommand(self.view, command)



# utility
class Ginput(sublime_plugin.TextCommand):
  def run(self, edit, format=None, prompt=False):
    if prompt:
      self.view.window().show_input_panel(
        """"gradle" + """,
        str(format) if format else '',
        partial(self.run, edit),
        None, None
      )

    command = format
    RunCommand.runCommand(self.view, command)
      

    
class Gopentest(sublime_plugin.TextCommand):
  def run (self, edit) :
    targetAppPath = sublime.load_settings("Gradle.sublime-settings").get("utility").get('webBrowseApp')
    testFilePathOrEmpty = Gradle.getBuildFolderPath(self.view)
    
    print "This util only work on Mac."

    if (testFilePathOrEmpty[0]):
      #index.html位置を直書きという暴挙
      path = testFilePathOrEmpty[1] + """/reports/tests/index.html"""

      # 別スレッドで実行
      thread = BuildThread("open" + " " + "-a" + " " + targetAppPath + " " + path)
      thread.start()

      #監視 + 表示
      ThreadProgressObserver(thread, path)



# 実行コマンド
class RunCommand():
  @classmethod
  def runCommand(self, view, command) :
    gradle = Gradle.getGradlePath(view)
    buildFilePath = Gradle.getBuildDotGradle(view)

  	# 別スレッドで実行
    thread = BuildThread(gradle + " " + command + " " + buildFilePath)
    thread.start()

    #監視 + 表示
    ThreadProgressObserver(thread, command)
