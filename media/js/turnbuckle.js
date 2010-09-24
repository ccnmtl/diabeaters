function initTurnbuckle() {
  var menuItem = jQuery("a:contains('Social Work Guide')");
  if( location.href.indexOf("social_work_guide") == -1) {
    menuItem.siblings().hide();
  
    menuItem.toggle(
      function () { jQuery(this).siblings().show(); },
      function () { jQuery(this).siblings().hide(); }
    );
  }
  
  else {
    menuItem.toggle(
      function () { jQuery(this).siblings().hide(); },
      function () { jQuery(this).siblings().show(); }
    );
  }
}

jQuery(document).ready(initTurnbuckle);