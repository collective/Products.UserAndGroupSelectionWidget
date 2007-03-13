
// function to open the popup window
function userandgroupselect_openBrowser(portal_url, fieldId, groupName, enableSearch, fieldType, multiVal, close_window)
{
    if (-1 == close_window)
        close_window = 1 - multiVal
    Search = 0
    if (groupName != '') {
    	Search = 1
    }
    window.open(portal_url + '/userandgroupselect_popup?Search:int=' + Search + '&groupname='+ groupName + '&enableSearch:int=' + enableSearch + '&fieldId=' + fieldId + '&fieldType=' + fieldType + '&multiVal:int=' + multiVal + '&close_window:int='+close_window, 'memberselect_popup','dependent=yes,toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=500,height=550');
}

// function to return a reference from the popup window back into the widget
function userandgroupselect_setEntry(fieldId, fieldType, username, label, multiVal)
{
    // differentiate between the single and mulitselect widget
    // since the single widget has an extra label field.
  pos = label.indexOf(' ')
  email = label.slice(0, pos)
  fullname = label.slice(pos + 1)
  if (fieldType == 'id') {
    label = username+' ('+fullname+')'
    if (multiVal==0) {
        element=document.getElementById(fieldId)
        label_element=document.getElementById(fieldId + '_label')
        element.value=username
        label_element.value=label
     }  else {
         list=document.getElementById(fieldId)
         // check if the item isn't already in the list
          for (var x=0; x < list.length; x++) {
            if (list[x].value == username) {
              return false;
            }
          }         
          // now add the new item
          theLength=list.length;
          list[theLength] = new Option(label);
          list[theLength].selected='selected';
          list[theLength].value=username
     }
   } else {
     // email
     if (fieldType == 'nameemail') {
         label = '"' + fullname + '" <' + email + '>'
     } else {
         label = email
     }
     element=document.getElementById(fieldId)
     if (multiVal==0) {
         element.value=label
     }  else {
         element.value += label + '\n'
     }
   }
}

// function to clear the reference field or remove items
// from the multivalued reference list.
function userandgroupselect_removeEntry(widget_id, multi)
{
    if (multi) {
        list=document.getElementById(widget_id)
        for (var x=list.length-1; x >= 0; x--) {
          if (list[x].selected) {
            list[x]=null;
          }
        }
        for (var x=0; x < list.length; x++) {
            list[x].selected='selected';
          }        
    } else {
        element=document.getElementById(widget_id);
        label_element=document.getElementById(widget_id + '_label');
        label_element.value = "";
        element.value="";
    }
}

