$(document).ready(function() {
  console.log("hi!")

  // Client sidebar
  $('#sidebar').on('click', '#client-list>.item:not(.active)', function() {
      $('.active').removeClass('active');
      $(this).addClass('active');

      client_id = $(this).val();
      $('#main').load('client_info/', {client:client_id})
  })

  // Sort buttons
  $('#az').click(function(event) {
      selected_id = $(".active").val();
      $.post("get_clients/", {sort:'az'}, function(result) {
          $('#client-list').html(result)
          $('#client-list>.item').each(function() {
              console.log('here')
              if ($(this).val() == selected_id) {
                  $(this).addClass('active')
              }
          })
      })
  })

  $('#za').click(function() {
      selected_id = $(".active").val();
      $.post("get_clients/", {sort:'za'}, function(result) {
          $('#client-list').html(result)
          $('#client-list>.item').each(function() {
              if ($(this).val() == selected_id) {
                  $(this).addClass('active')
              }
          })
      })
  })

})
