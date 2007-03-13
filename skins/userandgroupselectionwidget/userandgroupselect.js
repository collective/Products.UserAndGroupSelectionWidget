function userandgroupselect_openBrowser(portal_url, groupId, multiVal) {
    var url = portal_url;
    url += '/userandgroupselect_popup?selectgroup=';
    url += groupId;
    url += '&multiVal:int=';
    url += multiVal;

    var defines = 'dependent=yes,';
    defines += 'toolbar=no,';
    defines += 'location=no,';
    defines += 'status=no,';
    defines += 'menubar=no,';
    defines += 'scrollbars=yes,';
    defines += 'resizable=yes,';
    defines += 'width=500,';
    defines += 'height=550';
    
    window.open(url,
                'userandgroupselect_popup',
                defines);
}

function userandgroupselect_setEntry(fieldId, fieldType, username, label, multiVal) {
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

