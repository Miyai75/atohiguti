
let login_status = document.getElementById("login_status"); //index.htmlのid = loginを取得
let user = Cookies.get('login_id');
console.log(user);

// login状態の時ログアウトするに変える
if(user){
    // login_status.innerHTML = "ログアウトする";
    // login.setAttribute('href','/'); //飛ばす先を'/'ていうところに変更
}