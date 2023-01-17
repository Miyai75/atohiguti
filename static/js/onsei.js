//音声認識
// SpeechRecognitionの準備
const SpeechRecognition = webkitSpeechRecognition || SpeechRecognition;
const recognition = new SpeechRecognition()

json = "./static/js/hoge.json";


recognition.lang = 'en-US' // 言語コードen-US
recognition.continuous = true;
// hantei = 3

$.getJSON(json, function(data,status){

// 発話検出時に呼ばれる
recognition.onresult = (event) => {
    utterance = event.results[0][0].transcript
    recognition.stop();


    // output2.innerHTML = utterance + "<br>"

    // utterance に文字起こし→その後html化
    console.log(utterance) 
    // console.log(output2)
    // var u =String(utterance);
    // var u = "hello";
    // console.log(utterance) 
    console.log(n)

    if (utterance == data[n-1].name){

        console.log("正解");
        output2.innerHTML = "<p>正解文:"+ data[n-1].name+"</p>" + "<p>あなたの発音:"+ utterance+"</p><br>"

        $( ".def").hide();
        $( ".top").hide();
        hantei.innerHTML="<img src='/static/img/higuchi-happy.png' width=60% height=100% style= 'display: block; margin: auto;'>"
        $( "#hantei").show();
        top2.innerHTML="<p>Perfect！</p><br>"


    }else{
        console.log("不正解");
        output2.innerHTML = "<p>正解文:"+ data[n-1].name+"</p>" + "<p>あなたの発音:"+ utterance+"</p><br>"
        $( ".def").hide();
        $( ".top").hide();
        hantei.innerHTML="<img src='/static/img/higuchi-odoroki.png' width=60% height=100% style= 'display: block; margin: auto;'>"
        $( "#hantei").show();
        top2.innerHTML="<p>Close！</p><br>"

        $( ".start").show(); 
        $( ".stop").show(); 

    }


    // 次へボタン表示
    if( $( ".btn").css( "display" )){
        $( ".btn").show();
        $( "#output2").show();

        }

    // 次へボタンを押したら、文字起こしを非表示
    function butotnClick(){
        $( "#output2").hide(); 
        $( "#hantei").hide(); 
        $( ".def").show();
        }  
        
        let button = document.getElementById('btnn');
        button.onclick = butotnClick;
    // console.log(output2.innerHTML)

return [output2.innerHTML, hantei.innerHTML, top2.innerHTML]
    //innerHTMLで出力
}
})



    //recognition.start();

    //録音スタート
function startbutton() {
    //console.log("start")
    // $( "#start").hide();

    recognition.start();
    // ここに音声認識スタートを描く
}

//録音ストップ
function stopbutton() {
    //console.log("stop")
    recognition.stop();
}

// $(".btn").on('click',function(){
//     if( $("#output2").css("display")){
//         $( "#output2").hide(); 
//        }  
// }
