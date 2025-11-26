using System.Threading.Tasks;
using CrewViewer.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using System.IO;
using Markdig;

namespace CrewViewer.Pages.Crews
{
    public class ExecutionLogModel : PageModel
    {
        private readonly CrewDbContext _context;

        public Execution? Execution { get; set; }
        public string? MarkdownContent { get; set; }
        public string? SummaryContent { get; set; }   // 👈 nouveau
        public string? MarkdownHtml { get; set; }
        public string? SummaryHtml { get; set; }
        


        public ExecutionLogModel(CrewDbContext context)
        {
            _context = context;
        }


        public async Task<IActionResult> OnGetAsync(int id)
        {
            Execution = await _context.Executions
                .Include(e => e.crew)
                .FirstOrDefaultAsync(e => e.id == id);

            if (Execution == null)
            {
                return NotFound();
            }


            // Pipeline Markdown (avec quelques extensions sympas)
            var pipeline = new MarkdownPipelineBuilder()
                .UseAdvancedExtensions()
                .Build();


            // SUMMARY depuis la DB
            SummaryContent = Execution.output_summary;
            if (!string.IsNullOrWhiteSpace(SummaryContent))
            {
                SummaryHtml = Markdown.ToHtml(SummaryContent, pipeline);
            }

            // CONTENU .MD complet
            if (!string.IsNullOrWhiteSpace(Execution.output_file_path) &&
                System.IO.File.Exists(Execution.output_file_path))
            {
                MarkdownContent = System.IO.File.ReadAllText(Execution.output_file_path);
                MarkdownHtml = Markdown.ToHtml(MarkdownContent, pipeline);
            }

           
            return Page();
        }

    }



}
