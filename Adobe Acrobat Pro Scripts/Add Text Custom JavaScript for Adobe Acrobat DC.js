var f = this.addField("customText", "text", this.pageNum, [500, 50, 600, 80]); // adds text form field.   edit pageNum for text box location
f.textFont = font.Garamond;
f.textSize = 24;
f.value = "Your Text Here"; // What the user has typed in as the value for the field we created in the first line
f.readonly = false; // Makes it editable
