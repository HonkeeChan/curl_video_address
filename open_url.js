var page = require('webpage').create();                                         
// video url must have http:// suffix
var videoUrl = phantom.args[0];
//var videoUrl = "http://v.youku.com/v_show/id_XMTc3NDkwOTE2MA==.html?spm=a2hww.20023042.m_223465.5~5~5~5~5~5~A&from=y1.3-idx-beta-1519-23042.223465.1-1"
var videoTitle = null;
var playVideo = null;
window.setTimeout(function(){
   phantom.exit();
},  3* 60 * 60 * 1000);

//it is a timer for the same page. 
//if it redirect to other video page because this video has finish
// we will kill the browser.
window.setInterval(function(){
    if(videoTitle != null && videoTitle != page.title){
	   //console.log(videoTitle);
        phantom.exit();
    }	
}, 1000);


page.open(videoUrl , function () {
    videoTitle = page.title;
    if(page.url.indexOf("youku.com") != -1){
        console.log("in youku.com");
        // page.evaluate(function() {
        //     console.log("in evaluate function");
        //     playVideo = document.getElementById('sMain');  
        //     playVideo.click();
        //     console.log(playVideo);
        // });
        // playVideo = document.getElementById('sMain').textContent;
        // console.log("in youku.com");
        
        //it is from youku.com
        //find the player div
    }
    console.log("finish load");
    console.log("video title: " + videoTitle);
});

//TODO: click the right for player faster.
// window.setInterval(function(){
//     if(playVideo){
//         console.log("click");
//         console.log(playVideo);
//         playVideo.click();
//     }
//     page.sendEvent('keypress', page.event.key.Right, null, null, null);
// }, 1000);
