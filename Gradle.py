# coding=UTF-8

import os
import sys
import sublime
import sublime_plugin
import subprocess
import shlex
import threading
import glob
import string


class Gradle(sublime_plugin.TextCommand):
	def run (self, edit) :
		print "welcome to Gradle!"


class GetBuildFolderPath (sublime_plugin.TextCommand):
  @classmethod
  # buildフォルダを実行時のファイルから探す
  def getBuildFolderPath (self, currentView):
    
    # 今のウインドウに存在するフォルダパスが取れる。全部開いてしまう。
    folders = currentView.window().folders()

    # 現在のファイル
    currentFile = currentView.file_name()

    for folder in folders:
      if currentFile.startswith(folder):  # フォルダの一致
        currentFolder = folder


    # buildフォルダを探す
    os.chdir(currentFolder)
    buildFolder = glob.glob("build")
    
    if (0 < len(buildFolder)):
      # 先頭のもの=プロジェクトのもっとも浅い階層にいるbuildフォルダを採用する。
      buildFolderPath = os.path.join(currentFolder, buildFolder[0])
      print "build folder found @",buildFolderPath
      return (True, "\""+buildFolderPath + "\"")

    else:
      print "no build-Folder found. run \"gradle test\" will generate build-Folder. return empty"
      return (False,)


# build.gradleを実行時のファイルから探す
class GetBuildFilePath (sublime_plugin.TextCommand):
  @classmethod
  def getBuildFilePath(self, currentView):
    # 今のウインドウに存在するフォルダパスが取れる。全部開いてしまう。
    folders = currentView.window().folders()

    # 現在のファイル
    currentFile = currentView.file_name()
    
    for folder in folders:
        if currentFile.startswith(folder):
            currentFolder = folder


    # build.gradleを探す
    os.chdir(currentFolder)
    buildDotGradles = glob.glob("build.gradle")

    if (0 < len(buildDotGradles)):
        # 先頭のもの=プロジェクトのもっとも浅い階層にいるbuild.gradleを採用する。
        buildFilePath = os.path.join(currentFolder, buildDotGradles[0])
        print "build.gradle found @",buildFilePath
        return "-b" + " " + "\""+buildFilePath + "\""

    else:
        print "no build.gradle found. return empty"
        return ""


# スレッド
class BuildThread(threading.Thread):
  def __init__(self, command):
    self.command = command
    
    
    threading.Thread.__init__(self)

  def run(self):
    # run command
    process = subprocess.Popen(shlex.split(self.command.encode('utf8')), stdout=subprocess.PIPE)
    for line in process.stdout:
      print line
    # # processの末尾をread 微妙にロックする、tailっぽい機構
    # while True:
    #   out = process.stdout.read(1)
    #   if out == '' and process.poll() != None:
    #       break
    #   if out != '':
    #       sys.stdout.write(out)
    #       sys.stdout.flush()


# this method is replica of Package Control. this is verrrry good Method for express "something is running".
class ThreadProgress():
  def __init__(self, thread, message, success_message):
    self.thread = thread

    self.message = message
    self.success_message = success_message
    
    self.addend = 1
    self.size = 8
    sublime.set_timeout(lambda: self.run(0), 100)

  def run(self, i):
    if not self.thread.is_alive():
        sublime.status_message(self.success_message)
        return

    before = i % self.size
    after = (self.size - 1) - before
    sublime.status_message('%s [%s=%s]' % \
        (self.message, ' ' * before, ' ' * after))

    # カーソルをふらふらさせる
    if not after:
        self.addend = -1
    if not before:
        self.addend = 1
    i += self.addend

    # 100後に再度実行
    sublime.set_timeout(lambda: self.run(i), 100)
