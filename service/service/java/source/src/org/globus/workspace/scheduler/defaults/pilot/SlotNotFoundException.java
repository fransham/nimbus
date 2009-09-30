/*
 * Copyright 1999-2008 University of Chicago
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy
 * of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

package org.globus.workspace.scheduler.defaults.pilot;

public class SlotNotFoundException extends Exception {

    public String slotid;
    public String nodename;
    public int vmid = -1;

    SlotNotFoundException() {
        super();
    }

    public SlotNotFoundException(String slotid) {
        super();
        this.slotid = slotid;
    }

    public SlotNotFoundException(int vmid) {
        super();
        this.vmid = vmid;
    }

    public SlotNotFoundException(String slotid, String nodename) {
        super();
        this.slotid = slotid;
        this.nodename = nodename;
    }
}