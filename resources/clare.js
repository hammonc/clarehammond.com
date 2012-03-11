function resizeContent() {
  if ($(window).width() > 1200) {
    $("#container").width($(window).width());
    $(".scroll-pane-arrows").width($(window).width() - 480);
  }
}

$(document).ready(function() {
    resizeContent();

    $(window).resize(function () { resizeContent() });

    $(".scroll-pane-arrows").jScrollPane({
      showArrows: true,
      horizontalGutter: 10
	  });

    $(".more").click(function() {
	$(this).parent().find(".concealed").show("blind", {} , 500 );
	$(this).hide();
	$(this).parent().find(".less").show();
	return false;
      });
    
    $(".less").click(function() {
	$(this).parent().find(".concealed").hide("blind", {} , 500 );
	$(this).parent().find(".more").show();
	$(this).hide();
	return false;
      });
    
    $(".concealed").hide();
    $(".less").hide();

    $(".film-clip-still").mouseenter(function() {
	$(this)[0].src = $(this)[0].src.replace(".jpg", "-hover.jpg");
      });

    $(".film-clip-still").mouseleave(function() {
	$(this)[0].src = $(this)[0].src.replace("-hover.jpg", ".jpg");
      });

    $(".thumbnail").mouseenter(function() {
	$(this).addClass("highlighted");
      });

    $(".thumbnail").mouseleave(function() {
	$(this).removeClass("highlighted");
      });

    $(".thumbnail").click(function() {
	$(".gallery-main")[0].src = $(this)[0].src.replace("-thumb", "");
	$("#credit").html("Image copyright " + $(this).attr("credit"));
      });

    $(".popupwindow").popupwindow();

    $("#subscribe").click(function() {
	if (($("#email").val() == "") || ($("#name").val() == "")) {
	    alert("Please enter both your name and an e-mail address.");
	    return false;
	}
    });

    $("#unsubscribe").click(function() {
	if (($("#email").val() == "") || ($("#name").val() == "")) {
	    alert("Please enter both your name and an e-mail address.");
	    return false;
	}
    });
  });
