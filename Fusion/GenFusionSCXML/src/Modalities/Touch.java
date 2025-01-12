/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Modalities;

import scxmlgen.interfaces.IModality;

/**
 *
 * @author nunof
 */
public enum Touch implements IModality{
    
    DISLIKE("[GESTURES][DISLIKE]", 0),
	LIKE("[GESTURES][LIKE]", 0),
	FULLSCREEN("[GESTURES][FULLS]",0),
	NORMALSCREEN("[GESTURES][NORMALS]",0),
	NEXTVIDEO("[GESTURES][NEXTV]",0),
	PREVIOUSVIDEO("[GESTURES][PREVIOUSV]",0),
	SLIDEDOWN("[GESTURES][SLIDED]",0),
	SLIDEUP("[GESTURES][SLIDEUP]",0),
	VOLUMEUP("[GESTURES][VOLUMEU]",0),
	VOLUMEDOWN("[GESTURES][VOLUMED]",0),

    // HELP("[GESTURES][HELP]",0),

    ;
    
    private String event;
    private int timeout;


    Touch(String m, int time) {
        event=m;
        timeout=time;
    }

    @Override
    public int getTimeOut() {
        return timeout;
    }

    @Override
    public String getEventName() {
        //return getModalityName()+"."+event;
        return event;
    }

    @Override
    public String getEvName() {
        return getModalityName().toLowerCase()+event.toLowerCase();
    }
    
}