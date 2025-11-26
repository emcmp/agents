using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations.Schema;

namespace CrewViewer.Models
{
    public class CrewDbContext : DbContext
    {
        public CrewDbContext(DbContextOptions<CrewDbContext> options)
            : base(options)
        {
        }

        public DbSet<Agent> agent { get; set; } = null!;
        public DbSet<Crew> crew { get; set; } = null!;
        public DbSet<CrewAgent> crew_agent { get; set; } = null!;
        public DbSet<TaskEntity> task { get; set; } = null!;
        public DbSet<CrewTask> crew_task { get; set; } = null!;
        public DbSet<Execution> Executions { get; set; } = null!;


        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // === Agent ===
            modelBuilder.Entity<Agent>(entity =>
            {
                entity.ToTable("agent");
                entity.HasKey(a => a.id);
            });

            // === Crew ===
            modelBuilder.Entity<Crew>(entity =>
            {
                entity.ToTable("crew");
                entity.HasKey(c => c.id);
            });

            // === CrewAgent (table de jointure) ===
            modelBuilder.Entity<CrewAgent>(entity =>
            {
                entity.ToTable("crew_agent");

                // clé composite = (crew_id, agent_id)
                entity.HasKey(ca => new { ca.crew_id, ca.agent_id });

                entity.HasOne(ca => ca.crew)
                      .WithMany(c => c.crew_agents)
                      .HasForeignKey(ca => ca.crew_id);

                entity.HasOne(ca => ca.agent)
                      .WithMany(a => a.crew_agents)
                      .HasForeignKey(ca => ca.agent_id);
            });

            // === Task ===
            modelBuilder.Entity<TaskEntity>(entity =>
            {
                entity.ToTable("task");
                entity.HasKey(t => t.id);
            });

            // === CrewTask ===
            modelBuilder.Entity<CrewTask>(entity =>
            {
                entity.ToTable("crew_task");
                entity.HasKey(ct => ct.id);

                entity.HasOne(ct => ct.crew)
                      .WithMany(c => c.crew_tasks)
                      .HasForeignKey(ct => ct.crew_id);

                entity.HasOne(ct => ct.task)
                      .WithMany(t => t.crew_tasks)
                      .HasForeignKey(ct => ct.task_id);

                entity.HasOne(ct => ct.agent)
                      .WithMany(a => a.crew_tasks)
                      .HasForeignKey(ct => ct.agent_id);
            });

          
            //=== Execution ===
            modelBuilder.Entity<Execution>(entity =>
            {
                entity.ToTable("execution");
                entity.HasKey(e => e.id);

                entity.HasOne(e => e.crew)
                      .WithMany(c => c.executions)
                      .HasForeignKey(e => e.crew_id);
            });


            base.OnModelCreating(modelBuilder);
        }
    }

    // ===================== ENTITÉS =====================

    public class Agent
    {
        // colonnes SQLite
        public int id { get; set; }                    // id
        public string code { get; set; } = null!;      // code
        public string name { get; set; } = null!;      // name
        public string role { get; set; } = null!;      // role
        public string goal { get; set; } = null!;      // goal
        public string? backstory { get; set; }         // backstory
        public int? llm_model_id { get; set; }         // llm_model_id
        public double? temperature { get; set; }       // temperature
        public int? max_tokens { get; set; }           // max_tokens
        public bool verbose { get; set; }              // verbose
        public bool allow_delegation { get; set; }     // allow_delegation
        public bool is_active { get; set; }            // is_active

        // navigations
        public ICollection<CrewAgent> crew_agents { get; set; } = new List<CrewAgent>();
        public ICollection<CrewTask> crew_tasks { get; set; } = new List<CrewTask>();
    }

    public class Crew
    {
        // colonnes SQLite
        public int id { get; set; }                    // id
        public string code { get; set; } = null!;      // code
        public string name { get; set; } = null!;      // name
        public string? description { get; set; }       // description
        public string orchestration { get; set; } = null!; // orchestration
        public bool is_active { get; set; }            // is_active
        public string created_at { get; set; } = null!; // created_at
        public string updated_at { get; set; } = null!; // updated_at

        [NotMapped]
        public int exec_count { get; set; }


        // navigations
        public ICollection<CrewAgent> crew_agents { get; set; } = new List<CrewAgent>();
        public ICollection<CrewTask> crew_tasks { get; set; } = new List<CrewTask>();
        public ICollection<Execution> executions { get; set; } = new List<Execution>();
    }

    public class CrewAgent
    {
        // colonnes SQLite
        public int crew_id { get; set; }   // crew_id
        public int agent_id { get; set; }  // agent_id
        public bool is_lead { get; set; }  // is_lead
        public int sort_order { get; set; } // sort_order

        // navigations
        public Crew crew { get; set; } = null!;
        public Agent agent { get; set; } = null!;
    }

    public class TaskEntity
    {
        // colonnes SQLite
        public int id { get; set; }                       // id
        public string code { get; set; } = null!;         // code
        public string name { get; set; } = null!;         // name
        public string description { get; set; } = null!;  // description
        public string expected_output { get; set; } = null!; // expected_output
        public string? output_file { get; set; }          // output_file
        public bool is_active { get; set; }               // is_active

        // navigations
        public ICollection<CrewTask> crew_tasks { get; set; } = new List<CrewTask>();
    }

    public class CrewTask
    {
        // colonnes SQLite
        public int id { get; set; }              // id
        public int crew_id { get; set; }         // crew_id
        public int task_id { get; set; }         // task_id
        public int? agent_id { get; set; }       // agent_id
        public int sort_order { get; set; }      // sort_order
        public bool is_entry_point { get; set; } // is_entry_point
        public string? input_template { get; set; } // input_template

        // navigations
        public Crew crew { get; set; } = null!;
        public TaskEntity task { get; set; } = null!;
        public Agent? agent { get; set; }
    }
    public class Execution
    {
        public int id { get; set; }
        public int crew_id { get; set; }
        public string started_at { get; set; } = null!;
        public string? finished_at { get; set; }
        public string status { get; set; } = null!;
        public string? input_json { get; set; }
        public string? output_summary { get; set; }
        public string? output_file_path { get; set; }
        public string? error_message { get; set; }

        public string? stdout { get; set; }   // 👈 même nom que la colonne
        public string? stderr { get; set; }   // 👈 idem

        public Crew? crew { get; set; }
    }


}
