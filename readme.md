### Readme 

To run this program, make sure to get the video id list output from the Google API and update the values in the .json files under the `music_playlist_content_details_jsons` dir.

After you have loaded the video id targets, then run `run.py` and the program will save the `.mp3` files to a directory called: `saved_mp3s`

Note that each time this program is run, it will clear out the contents of `saved_mp3s`.

Credit https://www.geeksforgeeks.org/download-video-in-mp3-format-using-pytube/

Resolve issue if you get SSL certificate errors:
https://stackoverflow.com/questions/68275857/urllib-error-urlerror-urlopen-error-ssl-certificate-verify-failed-certifica
(Run the script: `Install Certificates.command` on Mac)

To get the video Ids from a playlist: https://developers.google.com/youtube/v3/docs/playlistItems/list

`part` == `contentDetails`

`playlistId` == `PL7wM1mNLtae0EWWjVoBQyoYW2xEugMASX`

`maxResultsPerPage` == 1000

Note that you only get 50 results per response, so you need to use the next page token while one exists to get all videos - use the `pageToken` to get the next page of results. Then, we will parse these to get the video Ids that can then be used to download the mp3.


