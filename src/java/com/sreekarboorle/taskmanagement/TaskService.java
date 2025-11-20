package com.sreekarboorle.taskmanagement.service;

import com.sreekarboorle.taskmanagement.model.Task;
import com.sreekarboorle.taskmanagement.repository.TaskRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class TaskService {
    private final TaskRepository repo;

    public TaskService(TaskRepository repo) { this.repo = repo; }

    public List<Task> findAll() { return repo.findAll(); }
    public Optional<Task> findById(Long id) { return repo.findById(id); }
    public Task save(Task t) { return repo.save(t); }
    public void deleteById(Long id) { repo.deleteById(id); }
}
