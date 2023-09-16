function setParam(name, value) {
  var l = window.location;

  /* build params */
  var params = {};
  var x = /(?:\??)([^=&?]+)=?([^&?]*)/g;
  var s = l.search;
  for(var r = x.exec(s); r; r = x.exec(s))
  {
    r[1] = decodeURIComponent(r[1]);
    if (!r[2]) r[2] = '%%';
    params[r[1]] = r[2];
  }

  /* set param */
  params[name] = encodeURIComponent(value);

  /* build search */
  var search = [];
  for(var i in params)
  {
    var p = encodeURIComponent(i);
    var v = params[i];
    if (v != '%%') p += '=' + v;
    search.push(p);
  }
  search = search.join('&');

  /* execute search */
  l.search = search;
}
function printa(a) {
  var s = ""
  for(var i = 0; i < a.length; i++){
    if (a[i].slice(0, 2) == "NP" && a[i].slice(0, 2) == "XP") {
      s += '<a href="https://www.ncbi.nlm.nih.gov/protein/' + a[i].replace(/:.*/, "") + '">' + a[i] + '</a><br>'
    } else {
      s += '<a href="https://www.ncbi.nlm.nih.gov/nuccore/' + a[i].replace(/:.*/, "") + '">' + a[i] + '</a><br>'
    }
  }
  return s
}
$(document).ready(function() {
  $('[data-target="#modalCenter"]').click(function() {
    var button = $(this);
    var snp = button[0].parentNode.parentNode.firstElementChild.innerText
    $.ajax({
      url: 'api/snp/' + snp + '/hgvs',
      method: 'GET',
      dataType: 'json',
      success: function (data) {
        $('.modalCenterTitle').text(snp)
        $('.modal-body').html(printa(data.content));
      },
      error: function () {
        $('.modal-body').html('Failed to fetch data.');
      }
    });
  })
  $('#modalCenter').on('hidden.bs.modal', function (e) {
    $('.modalCenterTitle').html("")
    $('.modal-body').html('<div class="spinner-border" role="status"> <span class="sr-only">Loading...</span> </div>')
  })
})