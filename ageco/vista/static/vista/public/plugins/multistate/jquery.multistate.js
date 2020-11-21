/**
 * jQuery.multistate
 *
 * Copyright (c) 2017 Salvatore Sicali
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 * https://github.com/...
 *
 * Version: 0.1
 *
 */
(function($){
// multistatetext ----------------------------------------------
   $.fn.multistatetext = function( options ){

    //  Versione 1
    //  ...

    //  Versione 2
      var opts = $.extend( {}, $.fn.multistatetext.defaults, options );
      this.each( function () {
        var that = this;
        var self = $(this);
        var state = opts.initstate;
        var selected = false;

        self.addClass(opts.mltstClass).addClass(opts.mltstClass+'-'+ state);
        self.text(state);

        if (opts.onChange){
           self.on('multistatetext.change', opts.onChange);
        }
        if (opts.onSelect){
           self.on('multistatetext.select', opts.onSelect);
        }

        function getNextState( origstate ) {
          return opts.states[( $.inArray( origstate, opts.states ) + 1 ) % opts.states.length];
        }

        that.State = function ( newstate ){
           if(newstate !== undefined) {
            	self.removeClass( opts.mltstClass+'-'+ state );
            	state = newstate;
            	self.addClass( opts.mltstClass+'-'+ state );
              self.text(state);
            	self.trigger('multistatetext.change', [state]);
           }
           return state;
        }

        /*that.Toggle = function (sendcall = true){
           if( selected ) {
            	self.removeClass( opts.mltstClass+'-selected');
              selected = false;
           }else{
              self.addClass( opts.mltstClass+'-selected' );
              selected = true;
           }
           if (sendcall) self.trigger('multistatetext.select', selected);
           return selected;
        }*/

        self.on( "toggle", function( event ) {
            if ( self.is( '.'+opts.mltstClass+'-selected' ) ) {
                self.trigger( "unselected" );
                selected = false;
            } else {
                self.trigger( "selected" );
                selected = true;
            }
            self.trigger('multistatetext.select', selected);
            return selected
        }).on( "selected", function( event ) {
            self.addClass( opts.mltstClass+'-selected' );
        }).on( "unselected", function( event ) {
            self.removeClass( opts.mltstClass+'-selected' );
        });


        self.on(opts.changeOnEvent + '.multistatetext', function ( event ) {
          if (opts.selectable) { self.trigger('toggle');/*that.Toggle();*/ }
          else if (opts.changable) { that.State( getNextState( state ) ); }
          //else blocked!!
        });


      });
      return this;

   }

   $.fn.multistatetext.destroy = function () {
     $( this ).off( '.multistatetext' );
   }

   $.fn.multistatetext.defaults = {
     selectable: false,
     changable: true,
     initstate: 'B',
     states: ['A','B','C'],
     mltstClass: 'multistatetext',
     changeOnEvent: 'click',
     onChange: null,
     onSelect: null,
   };
//. multistatetext----------------------------------------------

// multistatematrix---------------------------------------------
// From https://stackoverflow.com/questions/4963053/focus-to-input-without-scrolling
  var cursorFocus = function(elem) {
    var x = window.scrollX, y = window.scrollY;
    elem.focus();
    window.scrollTo(x, y);
  }

  $.fn.multistatematrix=function(options){
    if (typeof options == 'string'){
    	var mltsm = $.data(this[0], 'multistatematrix');
    	if (!mltsm) throw "Cannot perform '" + options + "' on a multistatematrix prior to initialization!";
    	switch (options){
    		case 'open':
    			mltsm.open(mltsm.options.target ? mltsm.options.target : this.first());
    			break;
    		case 'close':
    			mltsm.open(mltsm.options.target ? mltsm.options.target : this.first());
    			break;
        case 'editable':
    			console.log('modificabile: ' + mltsm.toggleEditable(mltsm.options.target ? mltsm.options.target : this.first()));
    			break;
    	}
    	return this;
    }
    // Apply the specified options overriding the defaults
    options = $.extend({}, $.fn.multistatematrix.defaults, options);
    // Create a multistatematrix. One for all elements in this jQuery selector.
    // Since multistatematrix() can be called on multiple elements on one page, each call will create a unique multistatematrix
    return this.each(function(){
			var id = 'mltsm' + ($('.mltsm-wrapper').length + 1);
			var mltsm = {};
			// If an element with the generated unique multistatematrix id exists, the multistatematrix had been instantiated already.
			// Otherwise create a new one!
      if ($('#'+id).length == 0) {
  				/** @var mltsm jQuery object containing the entire multistatematrix */
  				mltsm = $('<div id="' + id + '"></div>').addClass('mltsm-wrapper');
  				mltsm.options = options;
          mltsm.matrix = options.matrix; // TODO ottimizza
          mltsm.selection = undefined;
  				/** @var grid jQuery object containing the grid for the multistatematrix: the head, the body, the foot, etc. */
  				var table = $(options.gridTpl).addClass('mltsm-grid');
  				    mltsm.grid = table;
  				/** @var head jQuery object containing the grid for the multistatematrix: the display, the buttons, etc. */
  				var head = $(options.headTpl).addClass('mltsm-head');
                mltsm.head = head;
                /** Row Title Colon*/
                var rowTitle = $(options.titleColTpl).attr('colspan', options.titleCol.length+2); //$('<div style="display:inline-block;"></div>');
                Object.entries(options.states).forEach(([index, item]) => {
                    rowTitle.append($('<div style="display:inline-block;"></div>') //TODO generalizza
                        .multistatetext({ states: Object.keys(options.states), initstate : index, changable: false }))
                          .append($('<div style="display:inline-block; padding-right:0.4em;"></div>').html(item)); //TODO generalizza
                });
                head.append($(options.rowTpl).addClass('mltsm-options').append(rowTitle));

                rowTitle = $(options.rowTpl).addClass('mltsm-title').append($(options.titleColTpl)); //<<< Corner empty!
                options.titleCol.forEach(function(item){  // columns titles
                    rowTitle.append($(options.titleColTpl).html(item));
                });
                head.append(rowTitle);
  				/** @var foot jQuery object containing the grid for the multistatematrix: the display, the buttons, etc. */
  				var foot = $(options.footTpl).addClass('mltsm-foot'); //TODO Sposta in funzione
                mltsm.foot = foot;
  				/** @var body jQuery object containing the grid for the multistatematrix: the display, the buttons, etc. */
  				var body = $(options.bodyTpl).addClass('mltsm-body');
  				    mltsm.body = body;

          table.append(head);
  				table.append(foot);
  				table.append(body);
          // Append the grid table to the mltsm element
  				mltsm.append(table);
          // Create the backdrop of the multistatematrix - an overlay for the main page
  				mltsm.append($(options.backgroundTpl).addClass('mltsm-overlay')/*.click(function(){mltsm.close($(this));})*/);
          // Attach events
          if (options.onChange){
  					mltsm.on('multistatematrix.change', options.onChange);
  				}
          if (options.onSelected){
  					mltsm.on('multistatematrix.selected', options.onSelected);
  				}
          // Append mltsm to DOM
  				(options.appendKeypadTo ? options.appendKeypadTo : $(document.body)).append(mltsm);
          //TODO multistatematrix id not completely instantiated, left body
          // Finally, once the multistatematrix is completely instantiated, trigger multistatematrix.create
  				mltsm.trigger('multistatematrix.create');
			} else {
  				// If the multistatematrix was already instantiated previously, just load it into the mltsm variable
  				// mltsm = $('#'+id);
			}
      $.data(this, 'multistatematrix', mltsm); //TODO Verifica l'utilità?? Fondamentale per la verifica del if iniziale
			// Make the target element readonly and save the multistatematrix id in the data-multistatematrix property. Also add the special mltsm-target CSS class.
			$(this).attr("readonly", true).attr('data-multistatematrix', id).addClass('mltsm-target');//.val(JSON.stringify(options.matrix));
      // Register a listener to open the multistatematrix on the event specified in the options
			$(this).bind(options.openOnEvent,function(){
				mltsm.open(options.target ? options.target : $(this));
			});

			// Define helper functions

      // add single row
      mltsm.addRow = function ( open = false ) {
          if ( ! mltsm.matrix ) { mltsm.matrix = [0]; }
          else { mltsm.matrix.push([]);	}
          mltsm.matrix[mltsm.matrix.length - 1] = Array(options.titleCol.length+1);
          mltsm.matrix[mltsm.matrix.length - 1][0] = "new";
          mltsm.matrix[mltsm.matrix.length - 1].fill(options.initstate, 1);
          mltsm.createBody();
          position(mltsm.find('.mltsm-grid'), options.position, options.positionX, options.positionY);
      };
      /**
			* Sets one value on matrix of the multistatematrix
			* @param jQuery object source
      * @param string value
			* @return jQuery object mltsm  TODO ????
			*/
			mltsm.setValue = function ( self, state ) {
				var row = self.data('row');
				var col = self.data('col');
				//console.log(row+" "+col+" > "+state);
				mltsm.matrix[row][col] = state;
				mltsm.trigger('multistatematrix.change', [state]);
				return mltsm.matrix; // TODO: ????
			};
      // save selected and unselect previous
      mltsm.select = function (self) {
        var row = self.data('row');
        var col = self.data('col');

        if (mltsm.selection == undefined)
        {
          $("[data-row='" + row + "'][data-col='" + col + "']").trigger('selected');
        }else{
          $("[data-row='" + mltsm.selection.row + "'][data-col='" + mltsm.selection.col + "']").trigger('unselected');
        }

        mltsm.selection ={ 'row': row, 'col': col };
        mltsm.trigger('multistatematrix.selected', [mltsm.matrix, mltsm.selection]);
        return mltsm.selection;
      };
			/**
			* Create rows of body in the multistatematrix
			* @param
			* @return jQuery object mltsm
			*/
			mltsm.createBody = function(){
        mltsm.body.empty();
				if ( mltsm.matrix ){
					options = mltsm.options;
					mltsm.matrix.forEach( function( item, r ){
							var row = $(options.rowTpl).addClass('mltsm-row');
							item.forEach( function( value, c ){ // create columns
									if (c == 0) {
										row.append($(options.titleRowTpl) // create row title
											.append($(options.displayTpl).attr('data-row', r).attr('data-col', c).attr('disabled', !options.editable )
												.val( value ).addClass('mltsm-display')
													.change(function () { mltsm.setValue($(this), $(this).val()) }))
										);
									} else {
                    var opts = {};
                    if (options.editable){  // create column editable or selectable
                        opts = { states: Object.keys(options.states), initstate : value,
  												            onChange:function ( event, state ) { mltsm.setValue($(this), state) } };
                    } else {
                        opts = { states: Object.keys(options.states), initstate : value, selectable : true,
  												            onSelect:function ( event, selected) { if (selected) { mltsm.select($(this)) } } };
                    }
										row.append($(options.cellTpl).attr('data-row', r).attr('data-col', c)
											.multistatetext(opts));
									}
							});
              if (options.editable){ // create button removerow
  							row.append($(options.cellTpl).addClass('bs-glyphicons').addClass('removerow')
                  .append($('<span class="glyphicon glyphicon-remove-sign"></span>').addClass('removebtn')
                    .click(function(){
    									mltsm.matrix.splice(r, 1);
    									mltsm.createBody();
    								})
                  )
                );
              }
							mltsm.body.append(row);
					});
          // set initselection selected
          if (!options.editable){
            delete (mltsm.selection);
            mltsm.select($("[data-row='" + options.initselection.row + "'][data-col='" + options.initselection.col + "']"));
          }
        }
        // TODO now the multistatematrix is really fully instantiated, you can now trigger multistatematrix.create
        // Finally, once the multistatematrix is completely instantiated, trigger multistatematrix.create
        //mltsm.trigger('multistatematrix.create');
				return mltsm;
			};
      // Call createBody to complete instantiation
			//mltsm.createBody(); //TODO mltsm.matrix non è inizializzata quindi non serve???
      /**
			* Create rows of foot in the multistatematrix
			* @param
			* @return jQuery object mltsm
			*/
      mltsm.createFoot = function(){
        mltsm.foot.empty();
        /** Row foot Menu Function */
        if (options.editable){
          foot.append($(options.rowTpl).append($(options.cellTpl).attr('colspan', options.titleCol.length+2).addClass('addrow') // Add Row
              .append($('<button type="button" class="btn btn-info btn-xs btn-block"></button>').html(options.textAddRow)) //TODO generalizza
                .click(function() { mltsm.addRow(); })))
          .append($(options.rowTpl)
            .append($(options.cellTpl).attr('colspan', options.titleCol.length+2)// Save adn Cancel
              .append($('<div class="btn-group"></div>') //TODO generalizza
              .append($('<button type="button" class="btn btn-success "></button>').html(options.textSave).addClass('save')) //TODO generalizza
              .append($('<button type="button" class="btn btn-default "></button>').html(options.textCancel).addClass('cancel'))/*.click(function(){ mltsm.close($(this)); })*/)
            ));
        }
      }
      // Switch from editable to not editable
      mltsm.toggleEditable = function(target){
          options.editable = options.editable ? false : true ;
          mltsm.open(target);
          return options.editable;
      }

      /**
			* Save and/or Closes the multistatematrix writing it's value to the given target element
			* @param jQuery object target
			* @return jQuery object mltsm
			*/
			mltsm.close = function(target, save = false){
				// If a target element is given, set it's value to the dipslay value of the multistatematrix. Otherwise just hide the multistatematrix
				if (target && save){
					if (target.prop("tagName") == 'INPUT'){
            target.val(JSON.stringify(mltsm.matrix));
					} else {
						target.html(JSON.stringify(mltsm.matrix));
					}
        }else{ //you have call close with false for cancel action, then reset or delete matrix
          // Load on mltsm.matrix with target values
					// var source = $(this).val();
					// if (source){	mltsm.matrix = JSON.parse(source); }
					// else { delete mltsm.matrix; }
				}
        delete mltsm.matrix;
        if (options.closable)
        {// Hide the multistatematrix and trigger multistatematrix.close

          mltsm.hide(); // TODO Call only if closable modality is true
  				mltsm.trigger('multistatematrix.close');
        }else{
          console.log('not close');
          mltsm.open(target);
        }
				// Trigger a change event on the target element if the value has really been changed
				// TODO check if the value has really been changed!
				if (target && target.prop("tagName") == 'INPUT'){
					target.trigger('change');
				}
				return mltsm;
			};

      /**
			* Opens the multistatematrix for a given target element optionally filling it with a given value
			* @param jQuery object target
			* @return jQuery object mltsm
			*/
			mltsm.open = function(target){
        // Load on mltsm.matrix with target values
        if (target.prop("tagName") == 'INPUT'){
          var source = $(target).val();
        } else {
          var source = $(target).html();
        }

				if (source){
          mltsm.matrix = JSON.parse(source);
          //Call createBody to refresh body matrix
          mltsm.createBody(); // <<<<<<<<<<<<<<<<<<<
        } else {
          //Add Row if source is empty
          delete mltsm.matrix;
          mltsm.addRow()
        }
        mltsm.createFoot();
        // Show the multistatematrix and position it on the page
				cursorFocus(mltsm.show().find('.save'));
				position(mltsm.find('.mltsm-grid'), options.position, options.positionX, options.positionY);
				// Register a click handler on the done button to update the target element
				// Make sure all other click handlers get removed. Otherwise some unwanted sideeffects may occur if the multistatematrix is
				// opened multiple times for some reason TODO Repeat this control in other handlers
        //TODO add close button to foot and change here
				$('#'+id+' .save').off('click');
				$('#'+id+' .save').on('click', function(e){
          mltsm.close(target, true);
          e.stopPropagation();
        }); // Save and close
        $('#'+id+' .cancel').off('click');
				$('#'+id+' .cancel').on('click', function(e){
          mltsm.close(target);
          e.stopPropagation();
        }); // close without save
        $('#'+id+' .mltsm-wrapper').off('click');
        $('#'+id+' .mltsm-wrapper').on('click', function(e){
          mltsm.close(target);
          e.stopPropagation();
        }); // close without save

        // Finally trigger multistatematrix.open
				mltsm.trigger('multistatematrix.open');
				return mltsm;
			};
    });
  };

  /**
	* Positions any given jQuery element within the page
	*/
  function position(element, mode, posX, posY) {
  	var x = 0;
  	var y = 0;
  	if (mode == 'fixed'){
        element.css('position','fixed');

        if (posX == 'left'){
        	x = 0;
        } else if (posX == 'right'){
        	x = $(window).width() - element.outerWidth();
        } else if (posX == 'center'){
        	x = ($(window).width() / 2) - (element.outerWidth() / 2);
        } else if ($.type(posX) == 'number'){
        	x = posX;
        }
        element.css('left', x);

        if (posY == 'top'){
        	y = 0;
        } else if (posY == 'bottom'){
        	y = $(window).height() - element.outerHeight();
        } else if (posY == 'middle'){
        	y = ($(window).height() / 2) - (element.outerHeight() / 2);
        } else if ($.type(posY) == 'number'){
        	y = posY;
        }
        element.css('top', y);
  	}
      return element;
  }

  // Default values for multistatematrix options
	$.fn.multistatematrix.defaults = {
    states: {'A':'scelta A', 'B':'scelta B', 'C':'scelta C'},
    initstate: 'C',
    titleCol: ['Lu', 'Ma', 'Me', 'Gi', 'Ve', 'Sa', 'Do'],
    matrix: undefined, //[['Rig1', 'A', 'B', 'A', 'C'], ['Rig2','B', 'C', 'A', 'B']],
    initselection: {'row':0, 'col':1},
    editable: false,
    closable: false,
    // DOM setting
		target: false,          // data source
		openOnEvent: 'click',   // event connected to your data
    appendKeypadTo: false,  // parent in the DOM
    // Tags Layout
		backgroundTpl: '<div></div>',
		gridTpl: '<table></table>',
		headTpl: '<thead></thead>',
		bodyTpl: '<tbody></tbody>',
		footTpl: '<tfoot></tfoot>',
    rowTpl: '<tr></tr>',
    cellTpl: '<td></td>',
    titleRowTpl: '<th></th>',
		titleColTpl: '<th></th>',
    displayTpl: '<input type="text" class="form-control"/>',
		buttonFunctionTpl: '<button class="btn-default btn" ></button>',
    // Label button
    textSave: 'Imposta sequenza',
		textAddRow: 'Aggiungi Riga',
		textCancel: 'Annulla',
		textRemove: '-',
		// Position setting
		position: '', //'fixed',
		positionX: 'center',
		positionY: 'middle',
    //Attached Event
    onChange: false,
    onSelected: false,
	};
//. multistatematrix---------------------------------------------

}(jQuery));
