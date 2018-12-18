// SIDEBAR
$(document).ready(function(){
  $('.button-collapse').sideNav({
      menuWidth: 300, // Default is 300
      edge: 'left', // Choose the horizontal origin
      closeOnClick: false, // Closes side-nav on <a> clicks, useful for Angular/Meteor
      draggable: true // Choose whether you can drag to open on touch screens
    }
  );
  // START OPEN
  $('.button-collapse').sideNav('show');
});
//Calendario
  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15,// Creates a dropdown of 15 years to control year
	clear: 'Borrar',
    format: 'dd-mm-yyyy' });

//Select
 $(document).ready(function() {
    $('select').material_select();
  });

 $(document).ready(function() {
  $('#start').on('change', function() {
    if ($(this).is(':checked')) {
      console.log('Start is checked');
    }
  });
});

//Slider
$('.carousel.carousel-slider').carousel({fullWidth: false});

 // Or with jQuery

  $(document).ready(function(){
    $('.slider').slider();
  });


