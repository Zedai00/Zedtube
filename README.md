<h1>Zedtube</h1>

#### [Video Demo](https://www.youtube.com/watch?v=ZgJBthhVI8I)

Zedtube is an online video downloader and converter that you can use to download download videos from most sites like youtube and and convert videos to your selected format.

### Made With These Technologies

  ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
  ![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
  ![JavaScript](https://img.shields.io/badge/-JavaScript-black?style=flat-square&logo=javascript)
  ![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)
  ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
  ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
  ![Heroku](https://img.shields.io/badge/-Heroku-430098?style=flat-square&logo=heroku)
  ![Docker](https://img.shields.io/badge/-Docker-black?style=flat-square&logo=docker)
  ![Git](https://img.shields.io/badge/-Git-black?style=flat-square&logo=git)
  ![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github)
  
### Front-End

I wanted to make the site look good and beautiful and i learned of bootstrap which has some amazing content so i thought of searching some themes of bootstrap and found out [Startbootstrap](https://startbootstrap.com/) which has amazing themes and after scrolling through its catalog i found out this great theme called [Freelancer](https://startbootstrap.com/theme/freelancer) So I chose this and then i removed lot of stuff then made my own css file and modified it to according to my needs. First Off all after removing stuff from the theme i used Python-Flask to make a layout with all the navbar and its buttons so that it stays in every page of my site and the i made a templates for Download, Convert, Waiting, and Error.
In Convert I Used [DropZoneJS](https://www.dropzone.dev/js/) Which Is A Beautiful JS Plugin To Upload Videos And It Also Shows The File Size And Progress.
In both Download and Convert i have made a progress bar by using [SocketIO](https://socket.io/) which receives progress from backend and then i manipulate it by js to change all the value for progress.
  
### Backend

  For Backend I Used [Python](https://www.python.org/) And [Flask](https://flask.palletsprojects.com/) Web Framework For The Website As It Was Thought In CS50 And Python Is Easy And I Also Copied Some Of Code From The Finance Pset To Get Started.

  First Off To Download The Video From Sites I Used [Youtube-Dl](https://github.com/ytdl-org/youtube-dl) API Which Is Very Easy To Use And Is Able To Dowload Videos From Most Sites You Can Find The Supported Sites [Here](https://ytdl-org.github.io/youtube-dl/supportedsites.html). I Couldn't Find A Way To Show Progress Bar Of Downloading Video So I Searched On Google And I Found This [Stackoverflow Question](https://stackoverflow.com/questions/58662397/python-how-do-i-get-the-download-percentage-from-youtube-dl-when-im-downloading) And The Marked Answer Worked So I Copied That And Modified It A Little.
  But Sending Progress In Real Time Was Tricky So I Found Out SocketIO With Which You Can Send And Receive Messages Instantly So I Used [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) On The Server Side To Send Progress And On The Client Side I Used [SocketIO](https://socket.io/) As JS Script And Changed Progress Variables.

  To Convert Video To Other Formats I Used FFMPEG And I Couldnt Find A Good API As Of Them Were Complicated So I Directly Used Subprocess To Run Shell Commands Of FFMPEG To Turn Video In Other Formats. For Progress Bar In This I Again Searched And I Found This [Stackoverflow Question](https://stackoverflow.com/questions/67386981/ffmpeg-python-tracking-transcoding-process) Which Uses Threading Which I Also Learned From This And  As Before I Used Flask-SocketIO And SocketIO To Send And Receive Progress And Finally Used `SendFromDirectory` To Send Files To The User In Both Download And Convert.

#### Steps To Download A Video
  
- Copy The Link Of The Video Like In Youtube Copy The URL or Share The Video And Copy Its Link
- Paste That Link In Input Field
- Choose The Extension You Want From The Extension Dropdown
- Click The Download Button
  Then It Will Start Donwloading A Video Showing A Progress Bar With Percentage
  And Then It Will Convert It To Your Selected Format.

#### Steps To Convert A Video

- Press The Upload Box Or Drag A Video File Here And It Will Be Selected And It Will Show Its Name And Size
- Choose A Format From The Dropdown Extension
- Click On Upload And Once You Click It Will Be Start Uploading And Will Show You A Progress Bar And A Tick Mark Once Completed Then It Will Redirect You To Show The Progress
- After The Progress Completed It Will Show You A Download Button Once Clicked Will Start Downloading Your Video With The Changed Format

#### Future Improvements

- I Want To Add Music Support Where If You Give It A Video Link Or Video File It Will Extract The Audio And You Will Be Able To Download The Audio With Format Of Your Liking
