# coding=UTF-8

import os
import signal
import sys
import sublime
import sublime_plugin
import subprocess
import shlex
import threading
import glob
import string

# Gradle plugin for SublimeText2
class Gradle(sublime_plugin.TextCommand):
  def run (self, edit) :
    print "Welcome to the GradlePlugin!"
    
    print " "
    
    print "----search gradle--------------------"
    print "gradle  : "
    self.getGradlePath(self.view)

    print " "
    
    print "----search build.gradle--------------------"
    print "build.gradle  : "
    self.getBuildDotGradle(self.view)
     
    
    print " "
    
    print "----search build-folder-path---------------"
    print "build-folder  :  "
    self.getBuildFolderPath(self.view)

  # buildフォルダを実行時のファイルから探す
  @classmethod
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
      print "no build-folder found. run \"gradle build (or) test\" will generate build-folder. return empty"
      return (False,)


  # build.gradle を探し、オプションをつけて返す
  @classmethod
  def getBuildDotGradle(self, currentView):
    result = Gradle.getFilePath(currentView, "build.gradle")
    if (result[0]): 
      return "-b" + " " + result[1]


  # gradlew/gradlew.bat を探し、パスを返す
  @classmethod
  def getGradlew(self, currentView):
    result_unix = Gradle.getFilePath(currentView, "gradlew")
    if (result_unix[0]) :
     return result_unix[1]

    result_win = self.getFilePath(currentView, "gradlew.bat")
    if (result_win[0]):
     return result_win[1]

    print "no gradlew (or) gradlew.bat found. return empty." 
    return ""
    
  
  # 目的のファイルを現在のフォルダで探す
  @classmethod
  def getFilePath(self, currentView, targetFileName):
    # 今のウインドウに存在するフォルダパスが取れる。全部開いてしまう。
    folders = currentView.window().folders()

    # 現在のファイル
    currentFile = currentView.file_name()
    
    for folder in folders:
        if currentFile.startswith(folder):
            currentFolder = folder


    # ターゲットを探す
    os.chdir(currentFolder)
    targets = glob.glob(targetFileName)

    if (0 < len(targets)):
        # 先頭のもの=プロジェクトのもっとも浅い階層にいるターゲットを採用する。
        filePath = os.path.join(currentFolder, targets[0])
        print targetFileName, "found @", filePath
        return (True, "\""+filePath + "\"")

    else:
        print "no", targetFileName, " found. return empty"
        return (False, "")


  # gradleを探し、採用する
  @classmethod
  def getGradlePath(self, currentView):
    isUseGradlew = sublime.load_settings("Gradle.sublime-settings").get('use_gradlew')
    if (isUseGradlew) :
      # 第一候補はgradlew
      the1stCandidate = self.getGradlew(currentView)
      if len(the1stCandidate) != 0:
        return the1stCandidate

    # 第二候補はインストールされているもの = 設定ファイルから読む
    the2ndCandidate = sublime.load_settings("Gradle.sublime-settings").get('gradlePath')
    print the2ndCandidate
    if len(the2ndCandidate) != 0:
      return the2ndCandidate

    print """Please set the path for gradle or set "use_gradlew = true" when you use gradlew in the project."""
    print """From SublimeText2 > Preferences > Package Settings > Gradle > Settings - Default (or) User ."""
    return ""


# スレッド
class BuildThread(threading.Thread):
  def __init__(self, command):
    self.command = command
    
    
    threading.Thread.__init__(self)

  def run(self):
    # run command
    self.process = subprocess.Popen(shlex.split(self.command.encode('utf8')), stdout=subprocess.PIPE, preexec_fn=os.setsid)
    for line in self.process.stdout:
      print line
    # # processの末尾をread 微妙にロックする、tailっぽい機構
    # while True:
    #   out = process.stdout.read(1)
    #   if out == '' and process.poll() != None:
    #       break
    #   if out != '':
    #       sys.stdout.write(out)
    #       sys.stdout.flush()

  def killed(self):
    os.killpg(self.process.pid, signal.SIGTERM)


# スレッドの監視と進捗表示を行う
class ThreadProgressObserver():
  def __init__(self, thread, message):
    # threadを生存確認のために保持
    self.thread = thread

    # メッセージ
    self.message = message

    self.addend = 1
    self.size = 8

    # 指定タイミング後にMainThreadで実行
    sublime.set_timeout(lambda: self.run(0), 100)

  def run(self, i):
    if not self.thread.is_alive():
      addition = ""
        
      sublime.status_message('gradle %s finished. %s' % (self.message, addition))
      return

      

    before = i % self.size
    after = (self.size - 1) - before
    sublime.status_message('gradle %s running... [%s=%s]' % \
        (self.message, ' ' * before, ' ' * after))

    # カーソルをふらふらさせる
    if not after:
        self.addend = -1
    if not before:
        self.addend = 1
    i += self.addend

    # 100後に再度実行(ループ)
    sublime.set_timeout(lambda: self.run(i), 100)
