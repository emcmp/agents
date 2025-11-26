using System.Threading.Tasks;
using CrewViewer.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using System.Diagnostics;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;

using Microsoft.Extensions.Configuration;

namespace CrewViewer.Pages.Crews
{
    public class DetailsModel : PageModel
    {
        private readonly CrewDbContext _context;
        private readonly IConfiguration _config;

        [BindProperty] 
        public string? RunUserInput { get; set; }


        public DetailsModel(CrewDbContext context, IConfiguration config)
        {
            _context = context;
            _config = config;
        }

        public Crew crew { get; set; } = null!;

        public async Task<IActionResult> OnGetAsync(int id)
        {
            var found = await _context.crew
                .Include(c => c.crew_agents)
                    .ThenInclude(ca => ca.agent)
                .Include(c => c.crew_tasks)
                    .ThenInclude(ct => ct.task)
                .Include(c => c.crew_tasks)
                    .ThenInclude(ct => ct.agent)
                .FirstOrDefaultAsync(c => c.id == id);

            if (found == null)
            {
                return NotFound();
            }

            crew = found;

            crew.exec_count = _context.Executions.Count(e => e.crew_id == id);
            
            return Page();
        }
        public async Task<IActionResult> OnPostRunAsync(int id)
        {
            // Recharger le crew depuis EF
            var crewEntity = await _context.crew.FirstOrDefaultAsync(c => c.id == id);
            if (crewEntity == null)
                return NotFound();

            // Construire l'objet d'inputs pour le crew
            var inputs = new
            {
                user_input = RunUserInput ?? "Test depuis CrewViewer"
            };

            var jsonInput = JsonSerializer.Serialize(inputs);

            // Lire la config
            var pythonExecutable = _config.GetValue<string>("PythonRunner:Executable") ?? "uv";
            var workingDirectory = _config.GetValue<string>("PythonRunner:WorkingDirectory");

            // Préparer le lancement de uv/python
            var psi = new ProcessStartInfo
            {
                FileName = pythonExecutable,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            // IMPORTANT : on lance uv depuis le dossier datadrivencrew
            if (!string.IsNullOrWhiteSpace(workingDirectory))
            {
                psi.WorkingDirectory = workingDirectory;
            }

            psi.ArgumentList.Add("run");
            psi.ArgumentList.Add("python");
            psi.ArgumentList.Add("-m");
            psi.ArgumentList.Add("datadrivencrew.run_from_db");
            psi.ArgumentList.Add("--crew-code");
            psi.ArgumentList.Add(crewEntity.code);
            psi.ArgumentList.Add("--input-json");
            psi.ArgumentList.Add(jsonInput);

            using var process = Process.Start(psi);
            if (process == null)
                throw new Exception("Impossible de démarrer le process Python (uv).");

            string stdOut = await process.StandardOutput.ReadToEndAsync();
            string stdErr = await process.StandardError.ReadToEndAsync();
            await process.WaitForExitAsync();

            // Aller chercher la dernière exécution pour ce crew
            var lastExec = await _context.Executions
                .Where(e => e.crew_id == crewEntity.id)
                .OrderByDescending(e => e.id)
                .FirstOrDefaultAsync();


            if (lastExec != null)
            {
                lastExec.stdout = stdOut;
                lastExec.stderr = stdErr;

                await _context.SaveChangesAsync();

                // Rediriger vers une page qui affiche le log à partir de la DB
                return RedirectToPage("ExecutionLog", new { id = lastExec.id });
            }

            // fallback si pas d'exécution trouvée (cas bizarre)
            return RedirectToPage(new { id = crewEntity.id });

        }

    }
}
