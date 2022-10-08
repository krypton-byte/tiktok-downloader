      localStorage.mode = localStorage.mode || 'white';
      document.getElementById('mode').setAttribute('class', 'fas fa-'+(localStorage.mode === 'black'?'sun':'moon'));
      function mode(m){
        const text = (m === 'dark'|| m === 'black')?'white':'black';
        const bgcolor =(m === 'dark'|| m === 'black')?'black':'white';
        document.getElementsByTagName('body')[0].style.backgroundColor = bgcolor;
        document.getElementsByTagName('input')[0].style.borderColor = bgcolor==='black'?'#0D6EFD':'';
        document.getElementsByTagName('input')[0].style.backgroundColor=bgcolor;
        document.getElementsByTagName('input')[0].style.color=text;
        document.getElementsByTagName('img')[0].style.filter = bgcolor === 'black'?'invert(90%)':'';
        if(document.getElementsByClassName('card').length){          
          document.getElementsByClassName('card')[0].style.backgroundColor = bgcolor;
          document.getElementsByClassName('card')[0].style.borderColor = bgcolor === 'black'?'#0D6EFD':'';
          document.getElementsByTagName('p')[0].style.color = text;
        }
        localStorage.mode = bgcolor;
        document.getElementById('mode').setAttribute('class', 'fas fa-'+(localStorage.mode === 'black'?'sun':'moon'));
        document.getElementById('mode').style.color=(localStorage.mode === 'white'?'black':'white');
        document.getElementsByClassName('modal')[0].style.backgroundColor = localStorage.mode === 'black'?'rgba(0, 0, 0, .8)':'rgba( 255, 255, 255, .8 )'
      }
      document.getElementById('wrapMode').onclick = () => {
        mode(localStorage.mode==='black'?'white':'dark');
      }
      mode(localStorage.mode)
      document.getElementById('submitter').onclick = function(){
        $('body').addClass("loading");
        fetch('info?'+(new URLSearchParams({url: document.getElementById('tiktokurl').value})), {
          method: 'GET'
        }).then(async function (response){
          const data = await response.json();
          data.msg && Swal.fire({ icon: 'error', title: 'Oops...', text: data.msg, showConfirmButton: false})
          if(data.legacy){
            $(".emptydiv").empty().append(`
                <div class="row justify-content-center" id="downgrup" style="padding-bottom: 100px;">
                  <div class="card" style="width: 20 rem;background-color:${localStorage.mode === 'black'?'black; border-color: #0D6EFD':'white'}">
                    <video class="card-img-top" alt="..." poster="${data.aweme_detail.video.origin_cover.url_list[0]}" style="padding-top:7px;" controls>
                      <source src="${data.aweme_detail.video.play_addr.url_list[0]}" type="video/mp4">
                    </video>
                    
                    <div class="card-body">
                      <h5 class="card-title"><a href="https://www.tiktok.com/@${data.aweme_detail.author.unique_id}">${data.aweme_detail.author.unique_id}</a></h5>
                      <p class="card-text ${localStorage.mode === 'black'?'text-white':'text-black'}">${data.aweme_detail.desc}</p>
                    </div>
                    ${data.aweme_detail.video.play_addr.url_list.map(function(x){
                      return '<a href="'+x+'" target="_blank" class="btn btn-primary"> Video </a>&nbsp;';
                    }).join('')}
                    <a href="${data.aweme_detail.music.play_url.uri}" target="_blank" class="btn btn-primary mb-3"> Music </a>
                  </div>
              </div>
            `)
            $("body").removeClass("loading");
          }else{
            fetch('mdown?'+(new URLSearchParams({url: document.getElementById('tiktokurl').value})), {
              method: 'GET'
            }).then(async (resp) => {
              const dj = await resp.json()
              $(".emptydiv").empty().append(`
              <div class="row justify-content-center" id="downgrup" style="padding-bottom: 100px;">
                <div class="card" style="width: 20 rem;background-color:${localStorage.mode === 'black'?'black; border-color: #0D6EFD':'white'}">
                  <video class="card-img-top" alt="..." poster="${data.cover}" style="padding-top:7px;" controls>
                    <source src="${dj[0].url}" type="video/mp4">
                  </video>
                  
                  <div class="card-body">
                    <h5 class="card-title"><a href="https://www.tiktok.com/@${data.author}">${data.author}</a></h5>
                    <p class="card-text ${localStorage.mode === 'black'?'text-white':'text-black'}">${data.caption}</p>
                  </div>
                  ${dj.slice(1).map(function(x){
                    return '<a href="'+x+'" target="_blank" class="btn btn-primary"> Video </a>&nbsp;';
                  }).join('')}
                </div>
            </div>
          `)
          $("body").removeClass("loading");
            })
          }
        }).catch(function (err){
          $("body").removeClass("loading");
        })
      }