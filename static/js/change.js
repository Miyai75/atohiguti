

$(function(){
$(".btn").on('click',function(){
    for( i=1; i<4; i++ ){
        if( i == 3 ){
            j = 1;
        }else{
            j = i + 1;
        }

    if( $( "#cm" + i ).css( "display" ) != "none" ){
        $( "#cm" + i ).hide();
        $( "#cm" + j ).show();
    break;
    }
                        }
    });
});
