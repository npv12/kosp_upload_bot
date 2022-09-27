use std::collections::HashMap;

pub struct CancelableTasks {
    cancel_tasks: HashMap<u32, bool>,
}

impl CancelableTasks {
    pub fn add_task(&mut self, id: u32) {
        self.cancel_tasks.insert(id, false);
    }
    pub fn cancel_task(&mut self, id: u32) {
        self.cancel_tasks.insert(id, true);
    }
    pub fn get_cancel_status(&self, id: u32) -> bool {
        self.cancel_tasks.get(&id).unwrap().clone()
    }
    pub fn new() -> Self {
        Self {
            cancel_tasks: HashMap::new(),
        }
    }
    pub fn clone(&self) -> Self {
        Self {
            cancel_tasks: self.cancel_tasks.clone(),
        }
    }
}