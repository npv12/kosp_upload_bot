use std::{
    collections::HashMap,
    sync::{Arc, Mutex},
};

pub struct CancelableCommands {
    cancel_cmds: Arc<Mutex<HashMap<i32, bool>>>,
}

impl CancelableCommands {
    fn lock(&self) -> std::sync::MutexGuard<HashMap<i32, bool>> {
        log::debug!("Locking cancel_cmds");
        self.cancel_cmds.lock().unwrap()
    }
    fn unlock(&self, guard: std::sync::MutexGuard<HashMap<i32, bool>>) {
        log::info!("Current tasks include: {:?}", guard);
        log::debug!("Unlocking cancel_cmds");
        drop(guard);
    }
    pub fn insert(&mut self, id: i32) {
        let mut guard = self.lock();
        guard.insert(id, false);
        self.unlock(guard);
    }
    pub fn cancel(&mut self, id: i32) {
        let mut guard = self.lock();
        guard.insert(id, true);
        self.unlock(guard);
    }
    pub fn get_cancel_status(&self, id: i32) -> bool {
        let guard = self.lock();
        let status = guard.get(&id).unwrap_or(&false).clone();
        self.unlock(guard);
        status
    }
    pub fn new() -> Self {
        Self {
            cancel_cmds: Arc::new(Mutex::new(HashMap::new())),
        }
    }
    pub fn remove(&mut self, id: i32) {
        let mut guard = self.lock();
        guard.remove(&id);
        self.unlock(guard);
    }
    pub fn clone(&self) -> Self {
        Self {
            cancel_cmds: self.cancel_cmds.clone(),
        }
    }
}
