//提问的显示
function putquestion(){
    console.debug(1)
  if($('.write-question-box').css('display') == 'none'){
     $('.write-question-box').css({display:'inline'})
  }else{
     $('.write-question-box').css({display:'none'})
  }
}
//提问的不显示
function cancel(){
  if($('.write-question-box').css('display') != 'none'){
     $('.write-question-box').css({display:'none'})
  }
}
