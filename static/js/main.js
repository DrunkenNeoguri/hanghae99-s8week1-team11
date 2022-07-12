let slideIdx = 0;
// 아래의 이벤트보다는 상단에 적게 하여 slideIdx 변수를 받아오는 데 값이 없다는 문제가 생기지 않도록 하자.
const prevbtn = document.querySelector('.container--image__prevbtn');
const nextbtn = document.querySelector('.container--image__nextbtn');
prevbtn.addEventListener("click", () => {setSlidesImage(-1)});
nextbtn.addEventListener("click", () => {setSlidesImage(1)});

window.onload = () => {
  changeSlide(slideIdx);
  const setTime = 3000;
  setInterval(() => {
    slideIdx = slideIdx +1;
    changeSlide(slideIdx);
  }, setTime);
}

const slotArray = document.querySelectorAll(".list__outerSlot");
// 슬롯에 해당하는 div들을 몽땅 가져온다.
window.addEventListener("scroll", fadeInSlot);
// 화면에 scroll fadein 함수를 적용한다.


function fadeInSlot() {
    for (let i = 0; i < slotArray.length; i++) {
        const elem = slotArray[i]
        const showDistance = elem.getBoundingClientRect().top - window.innerHeight + 20;
        // getBoundingClientRect - 요소의 현재 페이지 위치를 알아낼 수 있음.
        // slot의 현재 페이지의 상단 영역 - 화면의 안쪽 높이(padding)까지 합친 값
        // innerHeight = content height + padding height
        // 요소가 있는 위치의 상단값이 화면 높이 +20
        console.log(elem.getBoundingClientRect().top);
        console.log(window.innerHeight);
        console.log(showDistance);
        if (showDistance < 0) {
          elem.classList.add("inView");
        } else {
          elem.classList.remove("inView");
        }
    }
}

// 슬롯을 실행하자.
fadeInSlot();
  

function setSlidesImage (num) {
  slideIdx = slideIdx + num;
  changeSlide(slideIdx);
}


function changeSlide (num) {
  const slideList = document.getElementsByClassName('container--image__slides');
  const slideLength = slideList.length;
  console.log(slideLength);
  if ((slideIdx +1) > slideLength) {
    slideIdx = 0;
    num = 0;
    // 슬라이드의 마지막까지 갔다면 슬라이드 순서를 초기화
    // num 값으로 슬라이드 순서가 정해지므로 해당 값도 0으로 설정.
  } else if (num < 0) {
    slideIdx = (slideLength -1);
    num = (slideLength -1)
    // prev 버튼을 계속 눌러 -1이 될 경우,
    // 슬라이드의 가장 마지막 순서로 변경.
  }
  // 나머지 전부 display 없애고, 현재 슬라이드만 보이도록 함.

  
  for (let i = 0; i < slideLength; i++) {
    slideList[i].style.display = "none";
  }
  slideList[num].style.display = "block";
}

window.scroll = () => {

}

  // $(window).scroll( function(){
    // $('image').each( function(i){
      // var bottom_of_element = $(this).offset().top + $(this).outerHeight();
      // var bottom_of_window = $(window).scrollTop() + $(window).height();
