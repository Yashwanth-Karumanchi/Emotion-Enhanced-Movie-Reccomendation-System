console.log("hello world")
function called()
{
    console.log("hello bro")
}
$.ajax({
    url: "/predict",
    type: "GET",
    dataType: "json",
    success: function(data) {
        // do something with the received data dictionary
        console.log(data);
    },
    error: function(jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown);
    }
});
