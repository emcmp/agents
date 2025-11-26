using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Automation;
using System.Windows.Forms;
using System.Xml.Linq;

namespace UIAutomation
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }


        public void PostToCopilot(string message)
        {
            // Find the Copilot window by title (replace with actual window title)
            AutomationElement copilotWindow = AutomationElement.RootElement.FindFirst(
                TreeScope.Children,
                new PropertyCondition(AutomationElement.NameProperty, "Untitled conversation")
            );
            if (copilotWindow == null)
            {
                Console.WriteLine("Copilot window not found.");
                return;
            }
            // Find the chat textbox inside the window
            AutomationElement chatBox = copilotWindow.FindFirst(
                TreeScope.Descendants,
                new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Edit)
            );
            if (chatBox == null)
            {
                Console.WriteLine("Chat textbox not found.");
                return;
            }
            // Write new text
            var valuePattern = chatBox.GetCurrentPattern(ValuePattern.Pattern) as ValuePattern;
            valuePattern.SetValue(message);
            Console.WriteLine("Text posted successfully.");
        }

        public void PostToChatGPT()
        {
            // Find the Copilot window by title (replace with actual window title)
            AutomationElement chatGPTWindow = AutomationElement.RootElement.FindFirst(
                TreeScope.Children,
                new PropertyCondition(AutomationElement.NameProperty, "Lier gestion projet et LLM")
            );


            if (chatGPTWindow == null)
            {
                Console.WriteLine("chatGPTWindow window not found.");
                return;
            }
            Console.WriteLine($"============================================");

            var allBox = chatGPTWindow.FindAll(TreeScope.Children, Condition.TrueCondition);
            foreach (AutomationElement window in allBox)
            {
                string name = window.Current.Name;
                string className = window.Current.ClassName;
                int processId = window.Current.ProcessId;

                Console.WriteLine($"Title: {name}, Class: {className}, PID: {processId}");
            }

            FindRecursively(chatGPTWindow, 0);

            // Find the chat textbox inside the window
            AutomationElement chatBox = chatGPTWindow.FindFirst(
                TreeScope.Descendants,
                new PropertyCondition(AutomationElement.ControlTypeProperty, ControlType.Edit)
            );

            if (chatBox == null)
            {
                Console.WriteLine("Chat textbox not found.");
                return;
            }

            // Read current text
            var valuePattern = chatBox.GetCurrentPattern(ValuePattern.Pattern) as ValuePattern;
            Console.WriteLine("Current text: " + valuePattern.Current.Value);

            // Write new text
            valuePattern.SetValue("Hello from my C# app!");

            Console.WriteLine("Text posted successfully.");

        }
        public void FindRecursively(AutomationElement rootElement, int id)
        {
            var elements = rootElement.FindAll(TreeScope.Children, Condition.TrueCondition);

            //Console.WriteLine($"====== {rootElement.Current.Name} {id}================");
            foreach (AutomationElement element in elements)
            {
                id++;
                string name = element.Current.Name;
                string className = element.Current.ClassName;
                int processId = element.Current.ProcessId;

               
                if (element.GetSupportedPatterns().Contains(ValuePattern.Pattern))
                {
                    var valuePattern = element.GetCurrentPattern(ValuePattern.Pattern) as ValuePattern;
                    if (!valuePattern.Current.IsReadOnly)
                    {
                        Console.WriteLine($"Title: {name}, Class: {className}, PID: {processId}");
                        valuePattern.SetValue("TEST EM : " + id);
                    }
                }

                FindRecursively(element, id);
            }

        }
        private void button1_Click(object sender, EventArgs e)
        {
            PostToChatGPT();
        }
    }
}
