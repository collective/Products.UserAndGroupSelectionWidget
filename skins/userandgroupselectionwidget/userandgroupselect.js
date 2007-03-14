function userandgroupselect_openBrowser(portal_url,
                                        fieldId,
                                        groupId) {
    var url = portal_url;
    url += '/userandgroupselect_popup?fieldId=';
    url += fieldId;
    url += '&selectgroup=';
    url += groupId;

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

function userandgroupselect_setEntry(elem, fieldId, multi) {
    if (multi == 0) {
        var field = document.getElementById(fieldId);
        var field_label = document.getElementById(fieldId + '_label');
        field.value = elem.id;
        field_label.value = elem.value;
    } else {
        var list = document.getElementById(fieldId);
        // check if the item isn't already in the list
        for (var x = 0; x < list.length; x++) {
            if (list[x].value == elem.id) {
                return false;
            }
        }         
        // now add the new item
        var len = list.length;
        list[len] = new Option(elem.value);
        list[len].selected = 'selected';
        list[len].value = elem.id;
    }
}

function userandgroupselect_removeEntry(fieldId, multi) {
    if (multi == 0) {
        var field = document.getElementById(fieldId);
        var field_label = document.getElementById(fieldId + '_label');
        field.value = '';
        field_label.value = '';
    } else {
        var list = document.getElementById(FieldId);
        for (var x = list.length - 1; x >= 0; x--) {
            if (list[x].selected) {
                list[x] = null;
            }
        }
        for (var x = 0; x < list.length; x++) {
            list[x].selected = 'selected';
        }     
    }
}