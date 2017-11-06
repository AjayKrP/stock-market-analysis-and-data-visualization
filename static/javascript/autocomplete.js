$( function() {
    var availableTags = [
       "AA", "AAPL","AMZN","FB", "GOOGL", "TSLA", "MMM", "MSFT", "ABBV", "ABC", "ABT", "ACE", "ACN", "AGN", "ADBE", "ADM", "ADP", "ADSK", "ADT", "AEE", "AEP", "AES", "AET"
    ];
    $( "#tags" ).autocomplete({
      source: availableTags
    });
  } );