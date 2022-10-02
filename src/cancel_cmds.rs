use std::{collections::HashMap, sync::{Arc, Mutex}};

pub struct CancelableCommands {
    pub cancel_cmds: HashMap<i32, bool>,
}

unsafe impl Send for CancelableCommands {}

impl CancelableCommands {
    pub fn add_cmd(&mut self, id: i32) {
        self.cancel_cmds.insert(id, false);
    }
    pub fn cancel_cmd(&mut self, id: i32) {
        self.cancel_cmds.insert(id, true);
    }
    pub fn get_cancel_status(&self, id: i32) -> bool {
        self.cancel_cmds.get(&id).unwrap().clone()
    }
    pub fn new() -> Self {
        Self {
            cancel_cmds: HashMap::new(),
        }
    }
    pub fn drop_cmd(&mut self, id: i32) {
        log::info!("Dropping task {}", id);
        self.cancel_cmds.remove(&id);
    }
}

pub fn add_cmds(tasks: &Arc<Mutex<CancelableCommands>>, id: &i32) {
    let mut my_task = tasks.lock().unwrap();
    my_task.add_cmd(*id);
    log::debug!("Tasks: {:?}", my_task.cancel_cmds);
    drop(my_task);
}

pub fn drop_cmds(tasks: &Arc<Mutex<CancelableCommands>>, id: &i32) {
    let mut my_task = tasks.lock().unwrap();
    my_task.drop_cmd(*id);
    log::debug!("Tasks: {:?}", my_task.cancel_cmds);
    drop(my_task);
}

pub fn cancel_cmd(tasks: &Arc<Mutex<CancelableCommands>>, id: &i32) {
    let mut my_task = tasks.lock().unwrap();
    my_task.cancel_cmd(*id);
    log::debug!("Tasks: {:?}", my_task.cancel_cmds);
    drop(my_task);
}