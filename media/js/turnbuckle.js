
function hideMenu(event) {
  // child links need to still do their linky thing
  if(event.originalTarget.nodeName == "A") {
    var href = event.originalTarget.href;
    if(href.substr(href.length - 19) != "/social_work_guide/") {
      window.location = event.originalTarget.href;
      return;
    }
  }
  jQuery(this).children("ul").hide();
  jQuery(this).css("background", "url(/site_media/img/bullet_open.gif) no-repeat scroll left 4px transparent");
}

function showMenu(event) {
  // child links need to still do their linky thing
  if(event.originalTarget && event.originalTarget.nodeName == "A") {
    var href = event.originalTarget.href;
    if(href.substr(href.length - 19) != "/social_work_guide/") {
      window.location = event.originalTarget.href;
      return;
    }
  }
  jQuery(this).children("ul").show();
  jQuery(this).css("background", "url(/site_media/img/bullet_close.gif) no-repeat scroll left 4px transparent");
}

function initTurnbuckle() {
  var menuItem = jQuery("a:contains('Social Work Guide')");
  if( location.href.indexOf("social_work_guide") == -1) {
    menuItem.parent("li").css("background", "url(/site_media/img/bullet_open.gif) no-repeat scroll left 4px transparent");
    menuItem.siblings().hide();
    menuItem.parent("li").toggle(showMenu, hideMenu);
  }

  else {
    menuItem.parent("li").css("background", "url(/site_media/img/bullet_close.gif) no-repeat scroll left 4px transparent");
    menuItem.parent("li").toggle(hideMenu, showMenu);
  }
}

jQuery(document).ready(initTurnbuckle);
