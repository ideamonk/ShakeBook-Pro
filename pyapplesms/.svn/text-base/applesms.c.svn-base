/*
 *  applesms.c
 *  
 *  PyAppleSMS - Python module for Apple SMS (Sudden Motion Sensor)
 *  
 *  Copyright (C) 2006 Michele Ferretti. All rights reserved.
 *  michele.ferreti@gmail.com
 *  http://www.blackbirdblog.it
 *  
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or any later version.
 *  
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *  
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA	02111-1307, USA.
 */

#include <stdio.h>
#include <string.h>
#include <IOKit/IOKitLib.h>
#include <Python.h>


// The various SMS hardware that supports
enum sms_hardware {
    unknown = 0,
    powerbook = 1,
    ibook = 2,
    highrespb = 3,
    macbookpro = 4
};

// returns the value of SMS hardware present or unknown if no hardware is detected
int detect_sms();
int read_sms_raw(int type, int *x, int *y, int *z);

enum data_type {
    PB_IB,
    MBP
};

struct pb_ib_data {
    int8_t x;
    int8_t y;
    int8_t z;
    int8_t pad[57];
};

struct mbp_data {
    int16_t x;
    int16_t y;
    int16_t z;
    int8_t pad[34];
};

union motion_data {
    struct pb_ib_data pb_ib;
    struct mbp_data mbp;
};


// custom python error object
static PyObject *AppleSMSError;

// public module function, return a tuple with (x,y,z) coordinates
static PyObject* coords(PyObject *self, PyObject *args) {
    int x, y, z;
	int type;
	
	// discover hardware type (powerbook, ibook, hirespb, macbookpro)
	type = detect_sms();

	// launch exception if hardware is not supported
	if( type == unknown ){
		PyErr_SetString(AppleSMSError, "No motion sensor available");
		return 0;
	}

	// grab sensor raw coordinates
	int result = read_sms_raw(type, &x, &y, &z);

	// create exception if result is lower than 1
	if( result < 1 ){
		switch(result){
			case  0: PyErr_SetString(AppleSMSError, "Hardware type not supported"); break;
			case -1: PyErr_SetString(AppleSMSError, "IOServiceGetMatchingServices returned error"); break;
			case -2: PyErr_SetString(AppleSMSError, "No motion sensor available"); break;
			case -3: PyErr_SetString(AppleSMSError, "Could not open motion sensor device"); break;
			case -4: PyErr_SetString(AppleSMSError, "No coords"); break;
		}
	    return 0;
	}
	
	// build tuple to return
	return Py_BuildValue("(i,i,i)", x, y, z);
}

// module methods array
static PyMethodDef AppleSMSMethods[] = {
    {"coords",  coords, METH_VARARGS, "get coordinates from Apple Sudden Motion Sensor"},
    {NULL, NULL, 0, NULL}
};

// module initializer
PyMODINIT_FUNC initapplesms(void) {
    PyObject *m = Py_InitModule3("applesms", AppleSMSMethods, "Python module for Apple SMS (Sudden Motion Sensor)");

    AppleSMSError = PyErr_NewException("applesms.error", NULL, NULL);
    Py_INCREF(AppleSMSError);
    PyModule_AddObject(m, "error", AppleSMSError);
}


 /*
 *  UniMotion - Unified Motion detection for Apple portables.
 *
 *  Copyright (c) 2006 Lincoln Ramsay. All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License version 2.1 as published by the Free Software Foundation.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 *  Foundation Inc. 59 Temple Place, Suite 330, Boston MA 02111-1307 USA
 */

/*
 * HISTORY of Motion
 * Written by Christian Klein
 * Modified for iBook compatibility by Pall Thayer
 * Modified for Hi Res Powerbook compatibility by Pall Thayer
 * Modified for MacBook Pro compatibility by Randy Green
 * Disparate forks unified into UniMotion by Lincoln Ramsay
 */

// This license applies to the portions created by Cristian Klein.
/* motion.c
 *
 * a little program to display the coords returned by
 * the powerbook motion sensor
 *
 * A fine piece of c0de, brought to you by
 *
 *               ---===---
 * *** teenage mutant ninja hero coders ***
 *               ---===---
 *
 * All of the software included is copyrighted by Christian Klein <chris@5711.org>.
 *
 * Copyright 2005 Christian Klein. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author must not be used to endorse or promote
 *    products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 */

static int set_values(int type, int *kernFunc, char **servMatch, int *dataType)
{
    switch ( type ) {
        case powerbook:
            *kernFunc = 21;
            *servMatch = "IOI2CMotionSensor";
            *dataType = PB_IB;
            break;
        case ibook:
            *kernFunc = 21;
            *servMatch = "IOI2CMotionSensor";
            *dataType = PB_IB;
            break;
        case highrespb:
            *kernFunc = 21;
            *servMatch = "PMUMotionSensor";
            *dataType = PB_IB;
            break;
        case macbookpro:
            *kernFunc = 5;
            *servMatch = "SMCMotionSensor";
            *dataType = MBP;
            break;
        default:
            return 0;
    }

    return 1;
}

static int probe_sms(int kernFunc, char *servMatch, int dataType, void *data)
{
    kern_return_t result;
    mach_port_t masterPort;
    io_iterator_t iterator;
    io_object_t aDevice;
    io_connect_t  dataPort;

    IOItemCount structureInputSize;
    IOByteCount structureOutputSize;

    union motion_data inputStructure;
    union motion_data *outputStructure;

    outputStructure = (union motion_data *)data;

    result = IOMasterPort(MACH_PORT_NULL, &masterPort);

    CFMutableDictionaryRef matchingDictionary = IOServiceMatching(servMatch);

    result = IOServiceGetMatchingServices(masterPort, matchingDictionary, &iterator);

    if (result != KERN_SUCCESS) {
        return -1;
    }

    aDevice = IOIteratorNext(iterator);
    IOObjectRelease(iterator);

    if (aDevice == 0) {
        return -2;
    }

    result = IOServiceOpen(aDevice, mach_task_self(), 0, &dataPort);
    IOObjectRelease(aDevice);

    if (result != KERN_SUCCESS) {
        return 3;
    }

    switch ( dataType ) {
        case PB_IB:
            structureInputSize = sizeof(struct pb_ib_data);
            structureOutputSize = sizeof(struct pb_ib_data);
            break;
        case MBP:
            structureInputSize = sizeof(struct mbp_data);
            structureOutputSize = sizeof(struct mbp_data);
            break;
        default:
            return 0;
    }

    memset(&inputStructure, 0, sizeof(union motion_data));
    memset(outputStructure, 0, sizeof(union motion_data));

    result = IOConnectMethodStructureIStructureO(dataPort, kernFunc, structureInputSize,
                &structureOutputSize, &inputStructure, outputStructure);

    IOServiceClose(dataPort);

    if (result != KERN_SUCCESS) {
        return -4;
    }
    return 1;
}

int detect_sms()
{
    int kernFunc;
    char *servMatch;
    int dataType;
    union motion_data data;
    int i;

    for ( i = 1; ; i++ ) {
        if ( !set_values(i, &kernFunc, &servMatch, &dataType) )
            break;
        if ( probe_sms(kernFunc, servMatch, dataType, &data) == 1 )
            return i;
    }

    return unknown;
}

int read_sms_raw(int type, int *x, int *y, int *z)
{
    int kernFunc;
    char *servMatch;
    int dataType;
    union motion_data data;

    if ( !set_values(type, &kernFunc, &servMatch, &dataType) )
        return 0;
    if ( probe_sms(kernFunc, servMatch, dataType, &data) == 1 ) {
        switch ( dataType ) {
            case PB_IB:
                if ( x ) *x = data.pb_ib.x;
                if ( y ) *y = data.pb_ib.y;
                if ( z ) *z = data.pb_ib.z;
                break;
            case MBP:
                if ( x ) *x = data.mbp.x;
                if ( y ) *y = data.mbp.y;
                if ( z ) *z = data.mbp.z;
                break;
            default:
                return 0;
        }
        return 1;
    }
    return 0;
}
