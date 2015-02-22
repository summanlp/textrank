/* Lead developer: Raphaël Velt
 * Licensed under the MIT License
 * Translations by:
 *    Vicenzo Cosenza (Italian)
 *    Eduardo Ramos Ibáñez (Spanish)
 *    Jaakko Salonen (Finnish)
 *    Zeynep Akata (Turkish)
 *    Σωτήρης Φραγκίσκος (Greek)
 *    Martin Eckert (German)
 * */

// Namespace
var GexfJS = {
    lensRadius : 200,
    lensGamma : 0.5,
    graphZone : {
        width : 0,
        height : 0
    },
    oldGraphZone : {},
    params : {
        centreX : 400,
        centreY : 350,
        activeNode : -1,
        currentNode : -1
    },
    oldParams : {},
    minZoom : -3,
    maxZoom : 10,
    overviewWidth : 200,
    overviewHeight : 175,
    baseWidth : 800,
    baseHeight : 700,
    overviewScale : .25,
    totalScroll : 0,
    autoCompletePosition : 0,
    i18n : {
        "de": {
            "search" : "Suche Knoten",
            "nodeAttr" : "Attribute",
            "nodes" : "Knoten",
            "inLinks" : "Ankommende Verknüpfung von",
            "outLinks" : "Ausgehende Verknüpfung zu",
            "undirLinks" : "Ungerichtete Verknüpfung mit",
            "lensOn" : "Vergrößerungsmodus an",
            "lensOff" : "Vergrößerungsmodus aus",
            "edgeOn" : "Kanten anzeigen",
            "edgeOff" : "Kanten verstecken",
            "zoomIn" : "Vergrößern",
            "zoomOut" : "Verkleinern",
            "browserErr" : 'Ihr Browser kann die Seite nicht richtig anzeigen.<br />Wir empfehlen die Verwendung der neusten <a href="http://www.mozilla.com/" target="_blank">Firefox</a> oder <a href="http://www.google.com/chrome/" target="_blank">Chrome</a> Version.'
        },
        "el" : {
            "search" : "Αναζήτηση Κόμβων",
            "nodeAttr" : "Χαρακτηριστικά",
            "nodes" : "Κόμβοι",
            "inLinks" : "Εισερχόμενοι δεσμοί από",
            "outLinks" : "Εξερχόμενοι δεσμοί προς",
            "undirLinks" : "Ακατεύθυντοι δεσμοί με",
            "lensOn" : "Ενεργοποίηση φακού",
            "lensOff" : "Απενεργοποίηση φακού",
            "edgeOn" : "Εμφάνιση ακμών",
            "edgeOff" : "Απόκρυψη ακμών",
            "zoomIn" : "Μεγέθυνση",
            "zoomOut" : "Σμίκρυνση",
            "browserErr" : 'Ο περιηγητής σας δεν μπορεί να εμφανίσει σωστά αυτή τη σελίδα.<br />Σας προτείνουμε να χρησιμοποιήσετε την τελευταία έκδοση του <a href="http://www.mozilla.com/" target="_blank">Firefox</a> ή του <a href="http://www.google.com/chrome/" target="_blank">Chrome</a>'
        },
        "en" : {
            "search" : "Search nodes",
            "nodeAttr" : "Attributes",
            "nodes" : "Nodes",
            "inLinks" : "Inbound Links from :",
            "outLinks" : "Outbound Links to :",
            "undirLinks" : "Undirected links with :",
            "lensOn" : "Activate lens mode",
            "lensOff" : "Deactivate lens mode",
            "edgeOn" : "Show edges",
            "edgeOff" : "Hide edges",
            "zoomIn" : "Zoom In",
            "zoomOut" : "Zoom Out",
            "browserErr" : 'Your browser cannot properly display this page.<br />We recommend you use the latest <a href="http://www.mozilla.com/" target="_blank">Firefox</a> or <a href="http://www.google.com/chrome/" target="_blank">Chrome</a> version'
        },
        "es" : {
            "search" : "Buscar un nodo",
            "nodeAttr" : "Atributos",
            "nodes" : "Nodos",
            "inLinks" : "Aristas entrantes desde :",
            "outLinks" : "Aristas salientes hacia :",
            "undirLinks" : "Aristas no dirigidas con :",
            "lensOn" : "Activar el modo lupa",
            "lensOff" : "Desactivar el modo lupa",
            "edgeOn" : "Mostrar aristas",
            "edgeOff" : "Ocultar aristas",
            "zoomIn" : "Acercar",
            "zoomOut" : "Alejar",
            "browserErr" : 'Tu navegador no es capaz de mostrar esta p&aacute;gina correctamente.<br />Le recomendamos utilizar la &uacute;ltima versi&oacute;n de <a href="http://www.mozilla.com/" target="_blank">Firefox</a> o <a href="http://www.google.com/chrome/" target="_blank">Chrome</a>',
            "modularity_class" : "Clase de modularidad",
            "degree" : "Grado",
            "indegree" : "Grado de entrada",
            "outdegree" : "Grado de salida",
            "weighted degree" : "Grado ponderado",
            "weighted indegree" : "Grado de entrada ponderado",
            "weighted outdegree" : "Grado de salida ponderado",
            "closnesscentrality" : "Cercan&iacute;a",
            "betweenesscentrality" : "Intermediaci&oacute;n",
            "authority" : "Puntuaci&oacute;n de autoridad (HITS)",
            "hub" : "Puntuaci&oacute; de hub (HITS)",
            "pageranks" : "Puntuaci&oacute; de PageRank"
        },
        "fi" : {
            "search" : "Etsi solmuja",
            "nodeAttr" : "Attribuutit",
            "nodes" : "Solmut",
            "inLinks" : "Lähtevät yhteydet :",
            "outLinks" : "Tulevat yhteydet :",
            "undirLinks" : "Yhteydet :",
            "lensOn" : "Ota linssitila käyttöön",
            "lensOff" : "Poista linssitila käytöstä",
            "edgeOn" : "Näytä kaikki yhteydet",
            "edgeOff" : "Näytä vain valitun solmun yhteydet",
            "zoomIn" : "Suurenna",
            "zoomOut" : "Pienennä",
            "browserErr" : 'Selaimesi ei voi näyttää tätä sivua.<br />Suosittelemme käyttämään uusinta versiota <a href="http://www.mozilla.com/" target="_blank">Firefox</a>- tai <a href="http://www.google.com/chrome/" target="_blank">Chrome</a>-selaimesta'
        },
        "fr" : {
            "search" : "Rechercher un n&oelig;ud",
            "nodeAttr" : "Attributs",
            "nodes" : "N&oelig;uds",
            "inLinks" : "Liens entrants depuis :",
            "outLinks" : "Liens sortants vers :",
            "undirLinks" : "Liens non-dirigés avec :",
            "lensOn" : "Activer le mode loupe",
            "lensOff" : "Désactiver le mode loupe",
            "edgeOn" : "Afficher les sommets",
            "edgeOff" : "Cacher les sommets",
            "zoomIn" : "S'approcher",
            "zoomOut" : "S'éloigner",
            "browserErr" : 'Votre navigateur n\'est malheureusement pas compatible avec les fonctionnalités de ce site<br />Nous vous suggérons d\'utiliser une version récente de <a href="http://www.mozilla.com/" target="_blank">Firefox</a> ou <a href="http://www.google.com/chrome/" target="_blank">Chrome</a>',
            "modularity_class" : "Classe de modularité",
            "degree" : "Degr&eacute;",
            "indegree" : "&frac12; degr&eacute; int&eacute;rieur",
            "outdegree" : "&frac12; degr&eacute; ext&eacute;rieur",
            "weighted degree" : "Degr&eacute; pond&eacute;r&eacute;",
            "weighted indegree" : "&frac12; degr&eacute; int&eacute;rieur pond&eacute;r&eacute;",
            "weighted outdegree" : "&frac12; degr&eacute; ext&eacute;rieur pond&eacute;r&eacute;",
            "closnesscentrality" : "Centralit&eacute; de proximit&eacute;",
            "betweenesscentrality" : "Centralit&eacute; d'interm&eacute;diarit&eacute;",
            "authority" : "Score d'autorit&eacute; (HITS)",
            "hub" : "Score de hub (HITS)",
            "pageranks" : "Score de PageRank"
        },
        "it" : {
            "search" : "Cerca i nodi",
            "nodeAttr" : "Attributi",
            "nodes" : "Nodi",
            "inLinks" : "Link in entrata da :",
            "outLinks" : "Link in uscita verso :",
            "undirLinks" : "Link non direzionati con :",
            "lensOn" : "Attiva la lente d'ingrandimento",
            "lensOff" : "Disattiva la lente d'ingrandimento",
            "edgeOn" : "Mostra gli spigoli",
            "edgeOff" : "Nascondi gli spigoli",
            "zoomIn" : "Zoom in avanti",
            "zoomOut" : "Zoom indietro",
            "browserErr" : 'Il tuo browser non pu&ograve; visualizzare correttamente questa pagina.<br />Ti raccomandiamo l\'uso dell\'ultima versione di  <a href="http://www.mozilla.com/" target="_blank">Firefox</a> o <a href="http://www.google.com/chrome/" target="_blank">Chrome</a>'
        },
        "tr" : {
            "search" : "Düğüm ara",
            "nodeAttr" : "Özellikler",
            "nodes" : "Düğümler",
            "inLinks" : "Gelen bağlantılar",
            "outLinks" : "Giden bağlantılar",
            "undirLinks" : "Yönsüz bağlantılar",
            "lensOn" : "Merceği etkinleştir",
            "lensOff" : "Merceği etkisizleştir",
            "edgeOn" : "Kenar çizgilerini göster",
            "edgeOff" : "Kenar çizgilerini gizle",
            "zoomIn" : "Yaklaştır",
            "zoomOut" : "Uzaklaştır",
            "browserErr" : "Tarayıcınız sayfayı doğru bir biçimde görüntüleyemiyor.<br />En son Firefox veya Chrome sürümünü kullanmanızı tavsiye ederiz."
        }
    },
    lang : "en"
};

function strLang(_str) {
    var _l = GexfJS.i18n[GexfJS.lang];
    return ( _l[_str] ? _l[_str] : ( GexfJS.i18n["en"][_str] ? GexfJS.i18n["en"][_str] : _str.replace("_"," ") ) );
}

function replaceURLWithHyperlinks(text) {
    if (GexfJS.params.replaceUrls) {
        var _urlExp = /(\b(https?:\/\/)?[-A-Z0-9]+\.[-A-Z0-9.:]+(\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*)?)/ig,
            _protocolExp = /^https?:\/\//i;
        return text.replace(_urlExp, function(_found) {
            return '<a href="'
                + ( _protocolExp.test(_found) ? '' : 'http://' )
                + _found + '" target="_blank">'
                + _found.replace(_protocolExp,'')
                + "</a>";
        });
    }
    return text;
}

function displayNode(_nodeIndex, _recentre) {
    GexfJS.params.currentNode = _nodeIndex;
    if (_nodeIndex != -1) {
        var _d = GexfJS.graph.nodeList[_nodeIndex],
            _b = _d.coords.base,
            _str = '',
            _cG = $("#leftcolumn");
            _cG.animate({
                "left" : "0px"
            }, function() {
                $("#aUnfold").attr("class","leftarrow");
                $("#zonecentre").css({
                    left: _cG.width() + "px"
                });
            });
        _str += '<h3><div class="largepill" style="background: ' + _d.color.base +'"></div>' + _d.label + '</h3>';
        _str += '<h4>' + strLang("nodeAttr") + '</h4>';
        _str += '<ul><li><b>id</b> : ' + _d.id + '</li>';
        for (var i in _d.attributes) {
            _str += '<li><b>' + strLang(i) + '</b> : ' + replaceURLWithHyperlinks( _d.attributes[i] ) + '</li>';
        }
        _str += '</ul><h4>' + ( GexfJS.graph.directed ? strLang("inLinks") : strLang("undirLinks") ) + '</h4><ul>';
        for (var i in GexfJS.graph.edgeList) {
            var _e = GexfJS.graph.edgeList[i];
            if ( _e.target == _nodeIndex ) {
                var _n = GexfJS.graph.nodeList[_e.source];
                _str += '<li><div class="smallpill" style="background: ' + _n.color.base +'"></div><a href="#" onmouseover="GexfJS.params.activeNode = ' + _e.source + '" onclick="displayNode(' + _e.source + ', true); return false;">' + _n.label + '</a>' + ( GexfJS.params.showEdgeLabel && _e.label ? ' &ndash; ' + _e.label : '') + ( GexfJS.params.showEdgeWeight && _e.weight ? ' [' + _e.weight + ']' : '') + '</li>';
            }
        }
        if (GexfJS.graph.directed) _str += '</ul><h4>' + strLang("outLinks") + '</h4><ul>';
        for (var i in GexfJS.graph.edgeList) {
            var _e = GexfJS.graph.edgeList[i];
            if ( _e.source == _nodeIndex ) {
                var _n = GexfJS.graph.nodeList[_e.target];
                _str += '<li><div class="smallpill" style="background: ' + _n.color.base +'"></div><a href="#" onmouseover="GexfJS.params.activeNode = ' + _e.target + '" onclick="displayNode(' + _e.target + ', true); return false;">' + _n.label + '</a>' + ( GexfJS.params.showEdgeLabel && _e.label ? ' &ndash; ' + _e.label : '') + ( GexfJS.params.showEdgeWeight && _e.weight ? ' [' + _e.weight + ']' : '') + '</li>';
            }
        }
        _str += '</ul><p></p>';
        $("#leftcontent").html(_str);
        if (_recentre) {
            GexfJS.params.centreX = _b.x;
            GexfJS.params.centreY = _b.y;
        }
        $("#searchinput")
            .val(_d.label)
            .removeClass('grey');
    }
}

function updateWorkspaceBounds() {
    
    var _elZC = $("#zonecentre");
    var _top = {
        top : $("#titlebar").height() + "px"
    };
    _elZC.css(_top);
    
    $("#leftcolumn").css(_top);
    GexfJS.graphZone.width = _elZC.width();
    GexfJS.graphZone.height = _elZC.height();
    GexfJS.areParamsIdentical = true;
    
    for (var i in GexfJS.graphZone) {
        GexfJS.areParamsIdentical = GexfJS.areParamsIdentical && ( GexfJS.graphZone[i] == GexfJS.oldGraphZone[i] );
    }
    if (!GexfJS.areParamsIdentical) {
    
    $("#carte")
        .attr({
            width : GexfJS.graphZone.width,
            height : GexfJS.graphZone.height
        })
        .css({
            width : GexfJS.graphZone.width + "px",
            height : GexfJS.graphZone.height + "px"
        });
        for (var i in GexfJS.graphZone) {
            GexfJS.oldGraphZone[i] = GexfJS.graphZone[i];
        }
    }
}

function startMove(evt) {
    evt.preventDefault();
    GexfJS.dragOn = true;
    GexfJS.lastMouse = {
        x : evt.pageX,
        y : evt.pageY
    };
    GexfJS.mouseHasMoved = false;
}

function endMove(evt) {
    document.body.style.cursor = "default";
    GexfJS.dragOn = false;
    GexfJS.mouseHasMoved = false;
}

function onGraphClick(evt) {
    if (!GexfJS.mouseHasMoved) {
        displayNode(GexfJS.params.activeNode);
    }
    endMove();
}

function changeGraphPosition(evt, echelle) {
    document.body.style.cursor = "move";
    var _coord = {
        x : evt.pageX,
        y : evt.pageY
    };
    GexfJS.params.centreX += ( GexfJS.lastMouse.x - _coord.x ) / echelle;
    GexfJS.params.centreY += ( GexfJS.lastMouse.y - _coord.y ) / echelle;
    GexfJS.lastMouse = _coord;
}

function onGraphMove(evt) {
    evt.preventDefault();
    if (!GexfJS.graph) {
        return;
    }
    GexfJS.mousePosition = {
        x : evt.pageX - $(this).offset().left,
        y : evt.pageY - $(this).offset().top
    };
    if (GexfJS.dragOn) {
        changeGraphPosition(evt,GexfJS.echelleGenerale);
        GexfJS.mouseHasMoved = true;
    } else {
        GexfJS.params.activeNode = getNodeFromPos(GexfJS.mousePosition);
        document.body.style.cursor = ( GexfJS.params.activeNode != -1 ? "pointer" : "default" );
    }
}

function onOverviewMove(evt) {
    if (GexfJS.dragOn) {
        changeGraphPosition(evt,-GexfJS.overviewScale);
    }
}

function onGraphScroll(evt, delta) {
    GexfJS.totalScroll += delta;
    if (Math.abs(GexfJS.totalScroll) >= 1) {
        if (GexfJS.totalScroll < 0) {
            if (GexfJS.params.zoomLevel > GexfJS.minZoom) {
                GexfJS.params.zoomLevel--;
                var _el = $(this),
                    _off = $(this).offset(),
                    _deltaX = evt.pageX - _el.width() / 2 - _off.left,
                    _deltaY = evt.pageY - _el.height() / 2 - _off.top;
                GexfJS.params.centreX -= ( Math.SQRT2 - 1 ) * _deltaX / GexfJS.echelleGenerale;
                GexfJS.params.centreY -= ( Math.SQRT2 - 1 ) * _deltaY / GexfJS.echelleGenerale;
                $("#zoomSlider").slider("value",GexfJS.params.zoomLevel);
            }
        } else {
            if (GexfJS.params.zoomLevel < GexfJS.maxZoom) {
                GexfJS.params.zoomLevel++;
                GexfJS.echelleGenerale = Math.pow( Math.SQRT2, GexfJS.params.zoomLevel );
                var _el = $(this),
                    _off = $(this).offset(),
                    _deltaX = evt.pageX - _el.width() / 2 - _off.left,
                    _deltaY = evt.pageY - _el.height() / 2 - _off.top;
                GexfJS.params.centreX += ( Math.SQRT2 - 1 ) * _deltaX / GexfJS.echelleGenerale;
                GexfJS.params.centreY += ( Math.SQRT2 - 1 ) * _deltaY / GexfJS.echelleGenerale;
                $("#zoomSlider").slider("value",GexfJS.params.zoomLevel);
            }
        }
        GexfJS.totalScroll = 0;
    }
}

function initializeMap() {
    clearInterval(GexfJS.timeRefresh);
    GexfJS.oldParams = {};
    GexfJS.ctxGraphe.clearRect(0, 0, GexfJS.graphZone.width, GexfJS.graphZone.height);
    $("#zoomSlider").slider({
        orientation: "vertical",
        value: GexfJS.params.zoomLevel,
        min: GexfJS.minZoom,
        max: GexfJS.maxZoom,
        range: "min",
        step: 1,
        slide: function( event, ui ) {
            GexfJS.params.zoomLevel = ui.value;
        }
    });
    $("#overviewzone").css({
        width : GexfJS.overviewWidth + "px",
        height : GexfJS.overviewHeight + "px"
    });
    $("#overview").attr({
        width : GexfJS.overviewWidth,
        height : GexfJS.overviewHeight
    });
    GexfJS.timeRefresh = setInterval(traceMap,60);
    GexfJS.graph = null;
    loadGraph();
}

function loadGraph() {
    
    $.ajax({
        url: ( document.location.hash.length > 1 ? document.location.hash.substr(1) : GexfJS.params.graphFile ),
        dataType: "xml",
        success: function(data) {
            var _s = new Date();
            var _g = $(data).find("graph"),
                _nodes = _g.children().filter("nodes").children(),
                _edges = _g.children().filter("edges").children();
            GexfJS.graph = {
                directed : ( _g.attr("defaultedgetype") == "directed" ),
                source : data,
                nodeList : [],
                nodeIndexById : [],
                nodeIndexByLabel : [],
                edgeList : []
            };
            var _xmin = 1e9, _xmax = -1e9, _ymin = 1e9, _ymax = -1e9; _marge = 30;
            $(_nodes).each(function() {
                var _n = $(this),
                _pos = _n.find("viz\\:position,position"),
                _x = _pos.attr("x"),
                _y = _pos.attr("y");
                _xmin = Math.min(_x, _xmin);
                _xmax = Math.max(_x, _xmax);
                _ymin = Math.min(_y, _ymin);
                _ymax = Math.max(_y, _ymax);
            });
            
            var _echelle = Math.min( ( GexfJS.baseWidth - _marge ) / ( _xmax - _xmin ) , ( GexfJS.baseHeight - _marge ) / ( _ymax - _ymin ) );
            var _deltax = ( GexfJS.baseWidth - _echelle * ( _xmin + _xmax ) ) / 2;
            var _deltay = ( GexfJS.baseHeight - _echelle * ( _ymin + _ymax ) ) / 2;
            
            GexfJS.ctxMini.clearRect(0, 0, GexfJS.overviewWidth, GexfJS.overviewHeight);
            
            $(_nodes).each( function() {
                var _n = $(this),
                    _id = _n.attr("id"),
                    _label = _n.attr("label") || _id,
                    _d = {
                        id: _id,
                        label: _label
                    },
                    _pos = _n.find("viz\\:position,position"),
                    _x = _pos.attr("x"),
                    _y = _pos.attr("y"),
                    _size = _n.find("viz\\:size,size").attr("value"),
                    _col = _n.find("viz\\:color,color"),
                    _r = _col.attr("r"),
                    _g = _col.attr("g"),
                    _b = _col.attr("b"),
                    _attr = _n.find("attvalue");
                _d.coords = {
                    base : {
                        x : _deltax + _echelle * _x,
                        y : _deltay - _echelle * _y,
                        r : _echelle * _size
                    }
                };
                _d.color = {
                    rgb : {
                        r : _r,
                        g : _g,
                        b : _b
                    },
                    base : "rgba(" + _r + "," + _g + "," + _b + ",.7)",
                    gris : "rgba(" + Math.floor(84 + .33 * _r) + "," + Math.floor(84 + .33 * _g) + "," + Math.floor(84 + .33 * _b) + ",.5)"
                };
                _d.attributes = [];
                $(_attr).each(function() {
                    var _a = $(this),
                        _for = _a.attr("for");                    
                    _d.attributes[ _for ? _for : 'attribute_' + _a.attr("id") ] = _a.attr("value");
                });
                GexfJS.graph.nodeIndexById.push(_id);
                GexfJS.graph.nodeIndexByLabel.push(_label.toLowerCase());
                GexfJS.graph.nodeList.push(_d);
                GexfJS.ctxMini.fillStyle = _d.color.base;
                GexfJS.ctxMini.beginPath();
                GexfJS.ctxMini.arc( _d.coords.base.x * GexfJS.overviewScale , _d.coords.base.y * GexfJS.overviewScale , _d.coords.base.r * GexfJS.overviewScale + 1 , 0 , Math.PI*2 , true );
                GexfJS.ctxMini.closePath();
                GexfJS.ctxMini.fill();
            });
            
            $(_edges).each(function() {
                var _e = $(this),
                    _sid = _e.attr("source"),
                    _six = GexfJS.graph.nodeIndexById.indexOf(_sid);
                    _tid = _e.attr("target"),
                    _tix = GexfJS.graph.nodeIndexById.indexOf(_tid);
                    _w = _e.find('attvalue[for="weight"]').attr('value') || _e.attr('weight');
                    _col = _e.find("viz\\:color,color");
                if (_col.length) {
                    var _r = _col.attr("r"),
                        _g = _col.attr("g"),
                        _b = _col.attr("b");
                } else {
                    var _scol = GexfJS.graph.nodeList[_six].color.rgb;
                    if (GexfJS.graph.directed) {
                        var _r = _scol.r,
                            _g = _scol.g,
                            _b = _scol.b;
                    } else {
                        var _tcol = GexfJS.graph.nodeList[_tix].color.rgb,
                            _r = Math.floor( .5 * _scol.r + .5 * _tcol.r ),
                            _g = Math.floor( .5 * _scol.g + .5 * _tcol.g ),
                            _b = Math.floor( .5 * _scol.b + .5 * _tcol.b );
                    }
                }
                GexfJS.graph.edgeList.push({
                    source : _six,
                    target : _tix,
                    width : Math.max( GexfJS.params.minEdgeWidth, Math.min( GexfJS.params.maxEdgeWidth, ( _w || 1 ) ) ) * _echelle,
                    weight : parseFloat(_w || 0),
                    color : "rgba(" + _r + "," + _g + "," + _b + ",.7)",
                    label: _e.attr("label") || "",
                });
            });
            
            GexfJS.imageMini = GexfJS.ctxMini.getImageData(0, 0, GexfJS.overviewWidth, GexfJS.overviewHeight);
        
        //changeNiveau(0);
        }
    });
}

function getNodeFromPos( _coords ) {
    for (var i = GexfJS.graph.nodeList.length - 1; i >= 0; i--) {
        var _d = GexfJS.graph.nodeList[i];
        if (_d.visible && _d.withinFrame) {
            var _c = _d.coords.actual;
                _r = Math.sqrt( Math.pow( _c.x - _coords.x , 2) + Math.pow( _c.y - _coords.y , 2 ) );
            if ( _r < _c.r ) {
                return i;
            }
        }
    }
    return -1;
}

function calcCoord(x, y, coord) {
    var _r = Math.sqrt( Math.pow( coord.x - x , 2 ) + Math.pow( coord.y - y , 2 ) );
    if ( _r < GexfJS.lensRadius ) {
        var _cos = ( coord.x - x ) / _r;
        var _sin = ( coord.y - y ) / _r;
        var _newr = GexfJS.lensRadius * Math.pow( _r / GexfJS.lensRadius, GexfJS.lensGamma );
        var _coeff = ( GexfJS.lensGamma * Math.pow( ( _r + 1 ) / GexfJS.lensRadius, GexfJS.lensGamma - 1 ) );
        return {
            "x" : x + _newr * _cos,
            "y" : y + _newr * _sin,
            "r" : _coeff * coord.r
        };
    }
    else {
        return coord;
    }
}

function traceArc(contexte, source, target) {
    contexte.beginPath();
    contexte.moveTo(source.x, source.y);
    if (GexfJS.params.curvedEdges) {
        if ( ( source.x == target.x ) && ( source.y == target.y ) ) {
            var x3 = source.x + 2.8 * source.r;
            var y3 = source.y - source.r;
            var x4 = source.x;
            var y4 = source.y + 2.8 * source.r;
            contexte.bezierCurveTo(x3,y3,x4,y4,source.x + 1,source.y);
        } else {
            var x3 = .3 * target.y - .3 * source.y + .8 * source.x + .2 * target.x;
            var y3 = .8 * source.y + .2 * target.y - .3 * target.x + .3 * source.x;
            var x4 = .3 * target.y - .3 * source.y + .2 * source.x + .8 * target.x;
            var y4 = .2 * source.y + .8 * target.y - .3 * target.x + .3 * source.x;
            contexte.bezierCurveTo(x3,y3,x4,y4,target.x,target.y);
        }
    } else {
        contexte.lineTo(target.x,target.y);
    }
    contexte.stroke();
}

function traceMap() {
    updateWorkspaceBounds();
    if (!GexfJS.graph) {
        return;
    }
    var _identical = GexfJS.areParamsIdentical;
    GexfJS.params.mousePosition = ( GexfJS.params.useLens ? ( GexfJS.mousePosition ? ( GexfJS.mousePosition.x + "," + GexfJS.mousePosition.y ) : "out" ) : null );
    for (var i in GexfJS.params) {
        _identical = _identical && ( GexfJS.params[i] == GexfJS.oldParams[i] );
    }
    if (_identical) {
        return;
    } else {
        for (var i in GexfJS.params) {
            GexfJS.oldParams[i] = GexfJS.params[i];
        }
    }
    
    GexfJS.echelleGenerale = Math.pow( Math.SQRT2, GexfJS.params.zoomLevel );
    GexfJS.decalageX = ( GexfJS.graphZone.width / 2 ) - ( GexfJS.params.centreX * GexfJS.echelleGenerale );
    GexfJS.decalageY = ( GexfJS.graphZone.height / 2 ) - ( GexfJS.params.centreY * GexfJS.echelleGenerale );
    
    var _sizeFactor = GexfJS.echelleGenerale * Math.pow(GexfJS.echelleGenerale, -.15),
        _edgeSizeFactor = _sizeFactor * GexfJS.params.edgeWidthFactor,
        _nodeSizeFactor = _sizeFactor * GexfJS.params.nodeSizeFactor,
        _textSizeFactor = 1;
    
    GexfJS.ctxGraphe.clearRect(0, 0, GexfJS.graphZone.width, GexfJS.graphZone.height);
    
    if (GexfJS.params.useLens && GexfJS.mousePosition) {
        GexfJS.ctxGraphe.fillStyle = "rgba(220,220,250,0.4)";
        GexfJS.ctxGraphe.beginPath();
        GexfJS.ctxGraphe.arc( GexfJS.mousePosition.x , GexfJS.mousePosition.y , GexfJS.lensRadius , 0 , Math.PI*2 , true );
        GexfJS.ctxGraphe.closePath();
        GexfJS.ctxGraphe.fill();
    }
    
    var _centralNode = ( ( GexfJS.params.activeNode != -1 ) ? GexfJS.params.activeNode : GexfJS.params.currentNode );
    
    for (var i in GexfJS.graph.nodeList) {
        var _d = GexfJS.graph.nodeList[i];
        _d.coords.actual = {
            x : GexfJS.echelleGenerale * _d.coords.base.x + GexfJS.decalageX,
            y : GexfJS.echelleGenerale * _d.coords.base.y + GexfJS.decalageY,
            r : _nodeSizeFactor * _d.coords.base.r 
        };
        _d.withinFrame = ( ( _d.coords.actual.x + _d.coords.actual.r > 0 ) && ( _d.coords.actual.x - _d.coords.actual.r < GexfJS.graphZone.width ) && ( _d.coords.actual.y + _d.coords.actual.r > 0) && (_d.coords.actual.y - _d.coords.actual.r < GexfJS.graphZone.height) );
        _d.visible = ( GexfJS.params.currentNode == -1 || i == _centralNode || GexfJS.params.showEdges );
    }
    
    var _tagsMisEnValeur = [];
    
    if ( _centralNode != -1 ) {
        _tagsMisEnValeur = [ _centralNode ];
    }
    
    var _displayEdges = ( GexfJS.params.showEdges && GexfJS.params.currentNode == -1 );
    
    for (var i in GexfJS.graph.edgeList) {
        var _d = GexfJS.graph.edgeList[i],
            _six = _d.source,
            _tix = _d.target,
            _ds = GexfJS.graph.nodeList[_six],
            _dt = GexfJS.graph.nodeList[_tix];
        var _isLinked = false;
        if (_centralNode != -1) {
            if (_six == _centralNode) {
                _tagsMisEnValeur.push(_tix);
                _coulTag = _dt.color.base;
                _isLinked = true;
                _dt.visible = true;
            }
            if (_tix == _centralNode) {
                _tagsMisEnValeur.push(_six);
                _coulTag = _ds.color.base;
                _isLinked = true;
                _ds.visible = true;
            }
        }

        if ( ( _isLinked || _displayEdges ) && ( _ds.withinFrame || _dt.withinFrame ) &&  _ds.visible && _dt.visible ) {
            GexfJS.ctxGraphe.lineWidth = _edgeSizeFactor * _d.width;
            var _coords = ( ( GexfJS.params.useLens && GexfJS.mousePosition ) ? calcCoord( GexfJS.mousePosition.x , GexfJS.mousePosition.y , _ds.coords.actual ) : _ds.coords.actual );
            _coordt = ( (GexfJS.params.useLens && GexfJS.mousePosition) ? calcCoord( GexfJS.mousePosition.x , GexfJS.mousePosition.y , _dt.coords.actual ) : _dt.coords.actual );
            GexfJS.ctxGraphe.strokeStyle = ( _isLinked ? _d.color : "rgba(100,100,100,0.2)" );
            traceArc(GexfJS.ctxGraphe, _coords, _coordt);
        }
    }
    GexfJS.ctxGraphe.lineWidth = 4;
    GexfJS.ctxGraphe.strokeStyle = "rgba(0,100,0,0.8)";
    
    if (_centralNode != -1) {
        var _dnc = GexfJS.graph.nodeList[_centralNode];
        _dnc.coords.real = ( (GexfJS.params.useLens && GexfJS.mousePosition ) ? calcCoord( GexfJS.mousePosition.x , GexfJS.mousePosition.y , _dnc.coords.actual ) : _dnc.coords.actual );
    }
    
    for (var i in GexfJS.graph.nodeList) {
        var _d = GexfJS.graph.nodeList[i];
        if (_d.visible && _d.withinFrame) {
            if (i != _centralNode) {
                _d.coords.real = ( ( GexfJS.params.useLens && GexfJS.mousePosition ) ? calcCoord( GexfJS.mousePosition.x , GexfJS.mousePosition.y , _d.coords.actual ) : _d.coords.actual );
                _d.isTag = ( _tagsMisEnValeur.indexOf(parseInt(i)) != -1 );
                GexfJS.ctxGraphe.beginPath();
                GexfJS.ctxGraphe.fillStyle = ( ( _tagsMisEnValeur.length && !_d.isTag ) ? _d.color.gris : _d.color.base );
                GexfJS.ctxGraphe.arc( _d.coords.real.x , _d.coords.real.y , _d.coords.real.r , 0 , Math.PI*2 , true );
                GexfJS.ctxGraphe.closePath();
                GexfJS.ctxGraphe.fill();
            }
        }
    }
    
    for (var i in GexfJS.graph.nodeList) {
        var _d = GexfJS.graph.nodeList[i];
        if (_d.visible && _d.withinFrame) {
            if (i != _centralNode) {
                var _fs = _d.coords.real.r * _textSizeFactor;
                if (_d.isTag) {
                    if (_centralNode != -1) {
                        var _dist = Math.sqrt( Math.pow( _d.coords.real.x - _dnc.coords.real.x, 2 ) + Math.pow( _d.coords.real.y - _dnc.coords.real.y, 2 ) );
                        if (_dist > 80) {
                            _fs = Math.max(GexfJS.params.textDisplayThreshold + 2, _fs);
                        }
                    } else {
                        _fs = Math.max(GexfJS.params.textDisplayThreshold + 2, _fs);
                    }
                }
                if (_fs > GexfJS.params.textDisplayThreshold) {
                    GexfJS.ctxGraphe.fillStyle = ( ( i != GexfJS.params.activeNode ) && _tagsMisEnValeur.length && ( ( !_d.isTag ) || ( _centralNode != -1 ) ) ? "rgba(60,60,60,0.7)" : "rgb(0,0,0)" );
                    GexfJS.ctxGraphe.font = Math.floor( _fs )+"px Arial";
                    GexfJS.ctxGraphe.textAlign = "center";
                    GexfJS.ctxGraphe.textBaseline = "middle";
                    GexfJS.ctxGraphe.fillText(_d.label, _d.coords.real.x, _d.coords.real.y);
                }
            }
        }
    }
    
    if (_centralNode != -1) {
        GexfJS.ctxGraphe.fillStyle = _dnc.color.base;
        GexfJS.ctxGraphe.beginPath();
        GexfJS.ctxGraphe.arc( _dnc.coords.real.x , _dnc.coords.real.y , _dnc.coords.real.r , 0 , Math.PI*2 , true );
        GexfJS.ctxGraphe.closePath();
        GexfJS.ctxGraphe.fill();
        GexfJS.ctxGraphe.stroke();
        var _fs = Math.max(GexfJS.params.textDisplayThreshold + 2, _dnc.coords.real.r * _textSizeFactor) + 2;
        GexfJS.ctxGraphe.font = "bold " + Math.floor( _fs )+"px Arial";
        GexfJS.ctxGraphe.textAlign = "center";
        GexfJS.ctxGraphe.textBaseline = "middle";
        GexfJS.ctxGraphe.fillStyle = "rgba(255,255,250,0.8)";
        GexfJS.ctxGraphe.fillText(_dnc.label, _dnc.coords.real.x - 2, _dnc.coords.real.y);
        GexfJS.ctxGraphe.fillText(_dnc.label, _dnc.coords.real.x + 2, _dnc.coords.real.y);
        GexfJS.ctxGraphe.fillText(_dnc.label, _dnc.coords.real.x, _dnc.coords.real.y - 2);
        GexfJS.ctxGraphe.fillText(_dnc.label, _dnc.coords.real.x, _dnc.coords.real.y + 2);
        GexfJS.ctxGraphe.fillStyle = "rgb(0,0,0)";
        GexfJS.ctxGraphe.fillText(_dnc.label, _dnc.coords.real.x, _dnc.coords.real.y);
    }
    
    GexfJS.ctxMini.putImageData(GexfJS.imageMini, 0, 0);
    var _r = GexfJS.overviewScale / GexfJS.echelleGenerale,
        _x = - _r * GexfJS.decalageX,
        _y = - _r * GexfJS.decalageY,
        _w = _r * GexfJS.graphZone.width,
        _h = _r * GexfJS.graphZone.height;
    
    GexfJS.ctxMini.strokeStyle = "rgb(220,0,0)";
    GexfJS.ctxMini.lineWidth = 3;
    GexfJS.ctxMini.fillStyle = "rgba(120,120,120,0.2)";
    GexfJS.ctxMini.beginPath();
    GexfJS.ctxMini.fillRect( _x, _y, _w, _h );
    GexfJS.ctxMini.strokeRect( _x, _y, _w, _h );
}

function hoverAC() {
    $("#autocomplete li").removeClass("hover");
    $("#liac_"+GexfJS.autoCompletePosition).addClass("hover");
    GexfJS.params.activeNode = GexfJS.graph.nodeIndexByLabel.indexOf( $("#liac_"+GexfJS.autoCompletePosition).text().toLowerCase() );
}

function changePosAC(_n) {
    GexfJS.autoCompletePosition = _n;
    hoverAC();
}

function updateAutoComplete(_sender) {
    var _val = $(_sender).val().toLowerCase();
    var _ac = $("#autocomplete");
    if (_val != GexfJS.dernierAC || _ac.html() == "") {
        GexfJS.dernierAC = _val;
        var _strAC = "<div><h4>" + strLang("nodes") + "</h4><ul>";
        var _n = 0;
        for (var i in GexfJS.graph.nodeIndexByLabel) {
            var _l = GexfJS.graph.nodeIndexByLabel[i];
            if (_l.search(_val) != -1) {
                _strAC += '<li id="liac_' + _n + '" onmouseover="changePosAC(' + _n + ')"><a href="#" onclick="displayNode(\'' + i + '\', true); return false;"><span>' + GexfJS.graph.nodeList[i].label + '</span></a>';
                _n++;
            }
            if (_n >= 20) {
                break;
            }
        }
        GexfJS.autoCompletePosition = 0;
        _ac.html(_strAC + "</ul></div>");
    }
    hoverAC();
    _ac.show();
}

function updateButtonStates() {
    $("#lensButton").attr("class",GexfJS.params.useLens?"":"off")
        .attr("title", strLang( GexfJS.params.showEdges ? "lensOff" : "lensOn" ) );

    $("#edgesButton").attr("class",GexfJS.params.showEdges?"":"off")
        .attr("title", strLang( GexfJS.params.showEdges ? "edgeOff" : "edgeOn" ) );
}

function setParams(paramlist) {
    for (var i in paramlist) {
        GexfJS.params[i] = paramlist[i];
    }
}

$(document).ready(function() {
    
    var lang = (
        typeof GexfJS.params.language != "undefined" && GexfJS.params.language
        ? GexfJS.params.language
        : (
            navigator.language
            ? navigator.language.substr(0,2).toLowerCase()
            : (
                navigator.userLanguage
                ? navigator.userLanguage.substr(0,2).toLowerCase()
                : "en"
            )
        )
    );
    GexfJS.lang = (GexfJS.i18n[lang] ? lang : "en");
    
    if ( !document.createElement('canvas').getContext ) {
        $("#bulle").html('<p><b>' + strLang("browserErr") + '</b></p>');
        return;
    }
    
    updateButtonStates();
    
    GexfJS.ctxGraphe = document.getElementById('carte').getContext('2d');
    GexfJS.ctxMini = document.getElementById('overview').getContext('2d');
    updateWorkspaceBounds();
    
    initializeMap();
    
    window.onhashchange = initializeMap;
    
    $("#searchinput")
        .focus(function() {
            if ( $(this).is('.grey') ) {
                $(this).val('').removeClass('grey');
            }
        })
        .keyup(function(evt) {
            updateAutoComplete(this);
        }).keydown(function(evt){
            var _l = $("#autocomplete li").length;
            switch (evt.keyCode) {
                case 40 :
                    if (GexfJS.autoCompletePosition < _l - 1) {
                        GexfJS.autoCompletePosition++;
                    } else {
                        GexfJS.autoCompletePosition = 0;
                    }
                break;
                case 38 :
                    if (GexfJS.autoCompletePosition > 0) {
                        GexfJS.autoCompletePosition--;
                    } else {
                        GexfJS.autoCompletePosition = _l - 1;
                    }
                break;
                case 27 :
                    $("#autocomplete").slideUp();
                break;
                case 13 :
                    if ($("#autocomplete").is(":visible")) {
                        var _liac = $("#liac_"+GexfJS.autoCompletePosition);
                        if (_liac.length) {
                            $(this).val(_liac.find("span").text());
                        }
                    }
                break;
                default :
                    GexfJS.autoCompletePosition = 0;
                break;
            }
            updateAutoComplete(this);
            if (evt.keyCode == 38 || evt.keyCode == 40) {
                return false;
            }
        });
    $("#recherche").submit(function() {
        if (GexfJS.graph) {
            displayNode( GexfJS.graph.nodeIndexByLabel.indexOf($("#searchinput").val().toLowerCase()), true);
        }
        return false;
    });
    $("#carte")
        .mousemove(onGraphMove)
        .click(onGraphClick)
        .mousedown(startMove)
        .mouseout(function() {
            GexfJS.mousePosition = null;
            endMove();
        })
        .mousewheel(onGraphScroll);
    $("#overview")
        .mousemove(onOverviewMove)
        .mousedown(startMove)
        .mouseup(endMove)
        .mouseout(endMove)
        .mousewheel(onGraphScroll);
    $("#zoomMinusButton").click(function() {
        GexfJS.params.zoomLevel = Math.max( GexfJS.minZoom, GexfJS.params.zoomLevel - 1);
        $("#zoomSlider").slider("value",GexfJS.params.zoomLevel);
        return false;
    })
        .attr("title", strLang("zoomOut"));
    $("#zoomPlusButton").click(function() {
        GexfJS.params.zoomLevel = Math.min( GexfJS.maxZoom, GexfJS.params.zoomLevel + 1);
        $("#zoomSlider").slider("value",GexfJS.params.zoomLevel);
        return false;
    })
        .attr("title", strLang("zoomIn"));
    $(document).click(function(evt) {
        $("#autocomplete").slideUp();
    });
    $("#autocomplete").css({
        top: ( $("#searchinput").offset().top + $("#searchinput").outerHeight() ) + "px",
        left: $("#searchinput").offset().left + "px"
    });
    $("#lensButton").click(function () {
        GexfJS.params.useLens = !GexfJS.params.useLens;
        updateButtonStates();
        return false;
    });
    $("#edgesButton").click(function () {
        GexfJS.params.showEdges = !GexfJS.params.showEdges;
        updateButtonStates();
        return false;
    });
    $("#aUnfold").click(function() {
        var _cG = $("#leftcolumn");
        if (_cG.offset().left < 0) {
            _cG.animate({
                "left" : "0px"
            }, function() {
                $("#aUnfold").attr("class","leftarrow");
                $("#zonecentre").css({
                    left: _cG.width() + "px"
                });
            });
        } else {
            _cG.animate({
                "left" : "-" + _cG.width() + "px"
            }, function() {
                $("#aUnfold").attr("class","rightarrow");
                $("#zonecentre").css({
                    left: "0"
                });
            });
        }
        return false;
    });
});