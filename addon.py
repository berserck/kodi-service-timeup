import xbmc
import xbmcaddon
import xbmcgui

import datetime as dt

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')


class XBMCPlayer(xbmc.Player):
    def __init__(self, *args):
        self.play_flag = 0
        self.pause_flag = 0
        pass

    def onPlayBackStarted(self):
        xbmc.log("Autostop playback started", xbmc.LOGERROR)
        self.play_flag = 1
        self.pause_flag = 0
        xbmc.log(f"Autostop playback started play:{self.play_flag} pause:{self.pause_flag}", xbmc.LOGERROR)

    def onPlayBackPaused(self):
        self.play_flag = 0
        self.pause_flag = 1
        xbmc.log(f"Autostop playback paused play:{self.play_flag} pause:{self.pause_flag}", xbmc.LOGERROR)

    def onPlayBackResumed(self):
        self.play_flag = 1
        self.pause_flag = 0
        xbmc.log(f"Autostop playback resumed play:{self.play_flag} pause:{self.pause_flag}", xbmc.LOGERROR)

    def onPlayBackEnded(self):
        self.play_flag = 0
        self.pause_flag = 0
        xbmc.log(f"Autostop playback ended play:{self.play_flag} pause:{self.pause_flag}", xbmc.LOGERROR)

    def onPlayBackStopped(self):
        self.play_flag = 0
        self.pause_flag = 0
        xbmc.log("fAutostop playback stopped play:{self.play_flag} pause:{self.pause_flag}", xbmc.LOGERROR)


if __name__ == '__main__':
    today = dt.date.today()
    today_play_count = 0

    max_play_time_minutes = 2
    max_time = dt.time(21, 25, 0, 0)

    xbmc.log("Timeup addon service started.", xbmc.LOGINFO)
    xbmcgui.Dialog().ok(addonname, f"{addonname} addon service started.")
    monitor = xbmc.Monitor()
    player = XBMCPlayer()



    play_count_s = 0
    wait_time_s = 10
    while not monitor.abortRequested():
        if monitor.waitForAbort(wait_time_s):
            # Abort was requested while waiting. We should exit
            break

        cur_time = dt.datetime.now().time()
        cur_date = cur_date = dt.datetime.today().date()
        is_playing = player.isPlaying()

        if cur_date > today:
            xbmcgui.Dialog().ok(addonname, f'DEBUG: day passed from {today} to {cur_date}')
            play_count_s = 0

        if is_playing:
            play_count_s += wait_time_s
        else:
            # xbmcgui.Dialog().ok(addonname, 'DEBUG: not playing')
            pass

        xbmc.log("Timeup .", xbmc.LOGINFO)

        if cur_time > max_time and is_playing:
            # player.stop()
            player.pause()
            xbmcgui.Dialog().ok(addonname, f'Time up, it is after {max_time}')
        if play_count_s > max_play_time_minutes * 60 and is_playing:
            # player.stop()
            player.pause()
            xbmcgui.Dialog().ok(addonname, 'Time up, you watched all you can today')

        xbmc.log( f" DEBUG: {addonname} Late:{cur_time > max_time} View Time:{play_count_s}s of {max_play_time_minutes * 60} play_flag: {player.play_flag} player state: {is_playing} video: {xbmc.Player().isPlayingVideo()}", xbmc.LOGWARNING)
