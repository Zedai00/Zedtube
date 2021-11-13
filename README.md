<h1>Zedtube</h1>

#### <center>[Video Demo](https://www.youtube.com/watch?v=ZgJBthhVI8I)
#### <center>[Live URL](https://zedtube-cs50.herokuapp.com/) 

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
  In both Download and Convert i have made a progress bar by using [SocketIO](https://socket.io/) which receives progress from backend and then i manipulate it by js to change all the value for progress.
  
### Backend
  
### Downloader

  The Download Works By  
  #### Steps To Download A Video 
  
  - Copy The Link Of The Video Like In Youtube Copy The URL or Share The Video And Copy Its Link
  - Paste That Link In Input Field
  - Choose The Extension You Want From The Extension Dropdown
  - Click The Download Button
  Then It Will Start Donwloading A Video Showing A Progress Bar With Percentage\n
  And Then It Will Convert It To Your Selected Format.
