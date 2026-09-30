# -*- coding: utf-8 -*-
"""Generate the Prompt Motion user manual (English only for now).

Same approach as build_zap_viewer_manual.py: zap-doctor.html is the shell, so
the font embeds, CSS and sidebar stay identical to the Zap manuals. Only the
<main> content, <title>/<meta> and product links differ. Facts come from the
add-on's GETTING_STARTED.md, INSTALL.md and docs/BETA_NOTES.md.
"""
import io
import os
import re

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
TEMPLATE = os.path.join(REPO, "zap-doctor.html")
OUT = os.path.join(REPO, "prompt-motion.html")

PRODUCT_URL = "https://farax-creative.github.io/prompt-motion/superhive.html"
TITLE = "Prompt Motion — User Manual · Farax Creative"
DESC = ("User manual for Prompt Motion — text-to-motion for Blender rigs. "
        "Install, the local model server, rig setup, Library, prompts, Path, "
        "Start, Goal, Reach, Key Poses, Hands, clips and troubleshooting.")

EXTRA_CSS = """<style>
figure.demo video{width:100%; display:block; background:#000}
.pm-note{border-left:2px solid var(--zap); padding:2px 0 2px 14px; color:var(--ink-2); max-width:70ch}
</style>
"""


def demo(src, caption):
    return ('<figure class="demo"><video src="../prompt-motion/media/%s" '
            'autoplay muted loop playsinline preload="metadata"></video>'
            '<figcaption>%s</figcaption></figure>' % (src, caption))


CONTENT = """
  <div class="doc-head">
    <div class="kicker"><span class="pmt">&gt;</span> PROMPT MOTION / USER MANUAL</div>
    <h1>PROMPT MOTION</h1>
    <div class="doc-sub">TEXT-TO-MOTION FOR YOUR BLENDER RIG</div>
    <div class="doc-meta">v1.0.0 &middot; Blender 4.5+ &middot; Windows 10/11 x64 &middot; NVIDIA RTX</div>
  </div>

  <!-- 1 · AT A GLANCE -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">01</span> AT A GLANCE</div>
    <h2>Type it, get a clip</h2>
    <p class="lead">Prompt Motion animates a rig you already have. You describe a motion in a sentence, a local model generates it on your GPU, and the result is baked onto your armature as a normal Action.</p>
    <ol class="hook-steps">
      <li>Select your armature and press <strong>Start</strong> to run the local model server.</li>
      <li>Type what happens, for example <em>&ldquo;A person walks forward and sits down on a chair.&rdquo;</em></li>
      <li>Set a duration and press <strong>Generate</strong>. The take lands on your rig as its own Action.</li>
    </ol>
    <p>Everything lives in the 3D viewport sidebar (<strong>N</strong>), on the <strong>Prompt Motion</strong> tab. No account and no cloud service: the model runs on your machine.</p>
    """ + demo("hero.mp4", "<b>Generate</b> &mdash; a typed prompt baked onto the rig.") + """
  </section>

  <!-- 2 · REQUIREMENTS & INSTALL -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">02</span> REQUIREMENTS &amp; INSTALL</div>
    <h2>Requirements and install</h2>

    <h3>What you need</h3>
    <div class="ref">
      <div class="row"><p class="rt">System</p><p class="rd">Windows 10 or 11, 64-bit. Windows only.</p></div>
      <div class="row"><p class="rt">GPU</p><p class="rd">NVIDIA RTX 20, 30, 40 or 50 series. About 3 GB of VRAM with default settings (the text encoder runs on the CPU; you can move it to the GPU in Preferences).</p></div>
      <div class="row"><p class="rt">Driver</p><p class="rd">570 or newer (CUDA 12.8), or 528 or newer (CUDA 12.1). RTX 50 cards need the CUDA 12.8 build.</p></div>
      <div class="row"><p class="rt">Memory &amp; disk</p><p class="rd">16 GB RAM. About 50 GB free disk: runtime about 5 GB, model about 17 GB. Non-English prompts add a 3 GB or 15 GB translator.</p></div>
      <div class="row"><p class="rt">Blender</p><p class="rd">4.5 or newer. Python is installed for you.</p></div>
    </div>

    <h3>Install</h3>
    <ol class="steps">
      <li><code>Edit &gt; Preferences &gt; Add-ons</code>, install the release <code>.zip</code> and enable it.</li>
      <li>Open the sidebar, go to <strong>Prompt Motion &gt; Runtime Install</strong> and press <strong>Install Runtime</strong>. It takes 10&ndash;30 minutes. A PowerShell window shows the progress. A proxy is optional.</li>
      <li>Press <strong>Download Kimodo Model</strong>. About 17 GB, roughly 30 minutes. No account needed.</li>
    </ol>
    <p>Nothing is written into the add-on folder. The files go here:</p>
    <ul>
      <li>Runtime: <code>~/.kimodo_venv/</code></li>
      <li>Install log: <code>~/.kimodo_runtime/install.log</code></li>
      <li>Model: <code>~/.cache/huggingface/hub/</code></li>
    </ul>
    <p>Re-running the installer is safe. If you move the model, move the whole Hugging Face cache tree (including <code>refs/main</code> and <code>snapshots/</code>) and point <code>HF_HOME</code> at it.</p>
  </section>

  <!-- 3 · SERVER -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">03</span> SERVER</div>
    <h2>Start the local model server</h2>
    <ol class="steps">
      <li>Press <strong>Start</strong> at the top of the panel.</li>
      <li>Wait for <strong>Server ready</strong>. Until then the panel shows <strong>Server offline</strong>.</li>
      <li>The server keeps running until you stop it or close Blender.</li>
    </ol>
    <p>To free GPU memory, stop the server with the stop button next to <strong>Server ready</strong>, or from <strong>Tools</strong>. If the add-on was updated and the running server is older, the panel says so: press <strong>Stop Server</strong> and start it again.</p>
    <p class="pm-note">The <strong>Library</strong> does not need the server. Everything that generates new motion does.</p>
  </section>

  <!-- 4 · RIG SETUP -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">04</span> RIG SETUP</div>
    <h2>Rig setup</h2>
    <p class="lead">Select an armature. The panel matches its bones by name and structure and shows the preset it picked.</p>
    <p>Built-in presets: <strong>Mixamo</strong>, <strong>VRoid</strong>, <strong>MMD</strong>, <strong>Rigify</strong>, <strong>CloudRig</strong>, <strong>Auto-Rig Pro</strong>, <strong>DAZ Genesis 8</strong> and <strong>DAZ Genesis 9</strong>. Mixamo characters such as Y Bot are matched as they come.</p>

    <h3>Match Bones and the mapping table</h3>
    <ol class="steps">
      <li>Open <strong>Bone Mapping</strong> and press <strong>Match Bones</strong>.</li>
      <li>Check the rows. Fix any bone that was matched wrong. Rows marked <code>*</code> are the 15 core bones.</li>
      <li>Press <strong>Save as Preset</strong> to reuse the mapping. Presets are stored outside the add-on, so updates keep them.</li>
    </ol>
    <p>If core joints are missing, the panel shows <strong>Mapping rejected, will not bake</strong>. Nothing is written to your rig until the mapping passes.</p>
    """ + demo("retarget.mp4", "<b>Rig matching</b> &mdash; one motion on different rigs.") + """

    <h3>IK and FK</h3>
    <p>If a Rigify or CloudRig limb is set to IK, FK keys are ignored and the limbs look stuck. The panel warns: <strong>Limbs are on IK, so FK keys are ignored</strong>. Press <strong>Switch Limbs to FK</strong> in <strong>Tools</strong> to fix it in one step.</p>

    <h3>Good to know</h3>
    <ul>
      <li>Motion runs at 30 fps. Applying a clip sets the scene to 30 fps.</li>
      <li>Constraints on mapped bones still act after the bake.</li>
      <li><strong>Keep Arms Out of the Body</strong> (Preferences, on by default) pushes arms out of the torso.</li>
    </ul>
  </section>

  <!-- 5 · LIBRARY -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">05</span> LIBRARY</div>
    <h2>Library</h2>
    <p class="lead">Ten ready-made motions that work without the server, a GPU or the model download.</p>
    <p>Walk, run, idle, wave, jump, look around, clap, bow, pick up and phone call.</p>
    <ol class="steps">
      <li>Select your armature.</li>
      <li>Open <strong>Library</strong> and pick a motion.</li>
      <li>Press <strong>Apply to Character</strong>. The motion is baked as an Action.</li>
    </ol>
    <p>Built-in motions can't be deleted or renamed. Your own clips can be added with the bookmark button on a clip row (<strong>Save to Library</strong>). They are saved in <code>Documents\\Prompt Motion Library</code>; you can change the folder in Preferences.</p>
  </section>

  <!-- 6 · GENERATE -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">06</span> GENERATE</div>
    <h2>Generate from a prompt</h2>
    <ol class="steps">
      <li>Start the server and select the armature.</li>
      <li>Type a prompt under <strong>What happens</strong>. Short third-person sentences work best: <em>&ldquo;A person jumps over a gap.&rdquo;</em></li>
      <li>Set the duration.</li>
      <li>Press <strong>Generate</strong>.</li>
    </ol>
    <p>Generating takes seconds. Writing keys onto a large rig can take minutes, and there is no cancel yet.</p>

    <h3>Takes and seeds</h3>
    <ul>
      <li>Every take is its own Action. Earlier takes are kept.</li>
      <li>The seed is <code>-1</code> (random) by default. To repeat a take you like, open <strong>More Settings</strong> and press <strong>Keep</strong> next to its seed.</li>
      <li><strong>New Clip Like This</strong> on a Library motion fills in its prompt, seed and duration, so the next Generate gives the same clip. Change the wording or duration to vary it.</li>
    </ul>

    <h3>Other languages</h3>
    <p>Non-English prompts are translated to English first. The default translator is <strong>Local AI (Offline)</strong>. Online translators are off by default. <strong>Translate to English</strong> shows the result before you generate.</p>
  </section>

  <!-- 7 · PATH -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">07</span> PATH</div>
    <h2>Path</h2>
    <p class="lead">Make the character follow a curve.</p>
    <ol class="steps">
      <li>Pick a curve under <strong>Path</strong>, or press <strong>+</strong> to add one: straight, S, turn left or turn right.</li>
      <li>Choose a <strong>Pace</strong>: Walk, Brisk Walk or Run.</li>
      <li>Generate. The character moves to the start of the curve and follows it.</li>
    </ol>
    <ul>
      <li>The duration follows the curve length.</li>
      <li>If the prompt says walk but the pace needs a run, the panel warns you.</li>
      <li>A facing toggle lets the character sidestep or move backward along the path.</li>
      <li>Single-spline curves only. The status bar reports how closely the result followed the curve.</li>
      <li>A path works with a single prompt.</li>
    </ul>
    """ + demo("path.mp4", "<b>Path</b> &mdash; the character follows a curve.") + """
  </section>

  <!-- 8 · START -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">08</span> START</div>
    <h2>Start</h2>
    <p>Sets where the motion begins and which way the character faces.</p>
    <ol class="steps">
      <li>Press <strong>+</strong> next to <strong>Start</strong>. An arrow Empty named <code>PM_Start</code> appears at the 3D cursor.</li>
      <li>Move it, and rotate it with <strong>R Z</strong> to set the facing.</li>
    </ol>
    <p>Any object can be the Start; its &minus;Y axis counts as forward. The arrow is not rendered. Start is not used together with Path.</p>
  </section>

  <!-- 9 · GOAL & AVOID -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">09</span> GOAL &amp; AVOID</div>
    <h2>Goal and obstacle avoidance</h2>
    <p class="lead">Walk to a spot and go around things on the way.</p>
    <ol class="steps">
      <li>Press <strong>+</strong> next to <strong>Goal</strong>. An orange flag appears. Place it where the character should end up.</li>
      <li>Select the objects to walk around and press the arrow next to <strong>Avoid</strong>. They go into the <code>PM_Obstacles</code> collection.</li>
      <li>Press <strong>Plan Route</strong>. A route curve <code>PM_Route</code> is created and put into <strong>Path</strong>.</li>
      <li><strong>Smooth Path</strong> rounds off the corners. Then generate.</li>
    </ol>
    <ul>
      <li>Objects below the ankle or above the head are ignored.</li>
      <li>If the goal can't be reached, the route is refused.</li>
      <li>If the duration is too short for the route, the panel warns you.</li>
    </ul>
  </section>

  <!-- 10 · REACH -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">10</span> REACH</div>
    <h2>Reach <span class="tag free">beta</span></h2>
    <p>One hand touches an object.</p>
    <ol class="steps">
      <li>Press <strong>+</strong> next to <strong>Reach (beta)</strong>. A sphere named <code>PM_Target</code> appears. Place it.</li>
      <li>Choose the right or left hand and when the touch happens.</li>
      <li>Generate.</li>
    </ol>
    <p>Reach generates twice, so it takes about twice as long. It works with Start but not with Path. If the target is out of reach, the panel says how many centimetres short it is.</p>
  </section>

  <!-- 11 · KEY POSES -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">11</span> KEY POSES</div>
    <h2>Key Poses</h2>
    <p class="lead">Poses you key by hand. The generated motion passes through them.</p>
    <ol class="steps">
      <li>Pose the rig on a frame and key it (<strong>Add Key Here</strong> in <strong>Key Poses</strong>).</li>
      <li>Repeat on other frames. The panel shows <strong>Using your key poses</strong>.</li>
      <li>Type a prompt and generate. The motion is built around your keys.</li>
    </ol>
    <p>Key Poses don't work with Path or with several prompts.</p>
    """ + demo("pose.mp4", "<b>Key Poses</b> &mdash; the motion passes through hand-keyed frames.") + """
  </section>

  <!-- 12 · SEVERAL PROMPTS -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">12</span> SEQUENCE</div>
    <h2>Several prompts, one clip</h2>
    <ol class="steps">
      <li>Turn on the toggle next to <strong>What happens</strong>.</li>
      <li>Press <strong>Add Segment</strong> for each action and give each one its own duration.</li>
      <li>Generate. Segments play top to bottom as one clip.</li>
    </ol>
  </section>

  <!-- 13 · HANDS -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">13</span> HANDS</div>
    <h2>Hands</h2>
    <p>Choose a hand pose: <strong>Relaxed</strong> (default), <strong>Fist</strong>, <strong>Hold</strong> or <strong>Rest</strong>. Use <strong>L / R</strong> to set each hand separately.</p>
    <p>The hand pose is one static pose for the whole clip. It is baked into the clip and fixed afterwards.</p>
  </section>

  <!-- 14 · CLIPS -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">14</span> CLIPS</div>
    <h2>Join, loop, NLA</h2>
    <div class="ref">
      <div class="row"><p class="rt">Join</p><p class="rd">Tick two or more clips and press <strong>Join Selected Clips</strong>. The seams are blended.</p></div>
      <div class="row"><p class="rt">Loop</p><p class="rd">The loop button on a clip row makes a looping copy named <code>&hellip;_loop</code>. Walks and runs keep moving forward. <strong>Repeats</strong> only sets how many cycles are shown.</p></div>
      <div class="row"><p class="rt">NLA</p><p class="rd"><strong>Add to Timeline</strong> puts a clip on the NLA as a strip on its own track, so several clips can share one timeline. Edit it in Blender's NLA editor.</p></div>
      <div class="row"><p class="rt">Clip row</p><p class="rd">The shield keeps the Action (Fake User). The bookmark saves it to the Library. <strong>Apply to</strong> puts the clip on the selected character.</p></div>
    </div>
  </section>

  <!-- 15 · TROUBLESHOOTING -->
  <section>
    <div class="sec-label"><span class="pmt">&gt;</span><span class="num">15</span> TROUBLESHOOTING</div>
    <h2>Troubleshooting</h2>
    <div class="ref">
      <div class="row"><p class="rt">Nothing happens when I press install</p><p class="rd">Turn on <code>Preferences &gt; System &gt; Network &gt; Allow Online Access</code>.</p></div>
      <div class="row"><p class="rt">The installer stops with a script error</p><p class="rd">PowerShell's ExecutionPolicy is blocking it. If <code>Get-ExecutionPolicy</code> says <code>Restricted</code>, run <code>Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned</code> once.</p></div>
      <div class="row"><p class="rt">Downloads time out</p><p class="rd">Check your bandwidth, firewall and proxy. Set a proxy or a mirror in the install options and run it again. Re-running does not start over.</p></div>
      <div class="row"><p class="rt">GatedRepoError</p><p class="rd">The public mirror for the text encoder was unavailable and the installer fell back to Meta's gated repository. Retry later, or accept the license on Hugging Face and log in with a read token.</p></div>
      <div class="row"><p class="rt">CUDA is not available</p><p class="rd">PyTorch and the driver disagree. Run <code>nvidia-smi</code> to see the CUDA version. RTX 50 cards need the cu128 build; RTX 30 and 40 work with cu121 or cu128.</p></div>
      <div class="row"><p class="rt">Install status looks wrong</p><p class="rd">Press <strong>Re-check</strong>. <strong>View Log</strong> opens the install log.</p></div>
      <div class="row"><p class="rt">Arms or legs don't move</p><p class="rd">The limbs are on IK. Press <strong>Switch Limbs to FK</strong> in <strong>Tools</strong>.</p></div>
      <div class="row"><p class="rt">Mapping rejected, will not bake</p><p class="rd">Core bones are missing. Press <strong>Match Bones</strong> and fill the rows marked <code>*</code>.</p></div>
      <div class="row"><p class="rt">Out of GPU memory</p><p class="rd">Stop the server when you're not generating. Keep the text encoder on the CPU (the default).</p></div>
      <div class="row"><p class="rt">Uninstall</p><p class="rd">Run <code>powershell -File installer/uninstall.ps1</code>.</p></div>
    </div>

    <h3>Not in this version</h3>
    <ul>
      <li>Stairs and uneven terrain.</li>
      <li>Two or more characters interacting.</li>
      <li>Jumping over obstacles on a route.</li>
      <li>Cancelling a bake that has started.</li>
    </ul>

    <h3>Getting help</h3>
    <p>Send a bug report with the Info log attached. Use the <strong>Report a Bug</strong> link below or email us.</p>

    <h3>Licenses</h3>
    <p>The add-on is GPL-3.0-or-later. Kimodo is Apache-2.0. The model weights are under the NVIDIA Open Model License. Built with Meta Llama 3.</p>
  </section>
"""


def build():
    shell = io.open(TEMPLATE, encoding="utf-8").read()
    head = shell[:shell.find('<main class="wrap">')]
    foot = shell[shell.find("<footer>"):]
    foot = re.sub(r"<script>\s*/\* Collapse All.*?</script>", "", foot,
                  flags=re.S)

    h = head
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, h, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")',
               r"\g<1>%s\g<2>" % DESC, h)
    # No translations yet, so drop the language switcher.
    h = re.sub(r'\s*<div class="lang-switch">.*?</ul>\s*</div>', "", h,
               flags=re.S)
    h = h.replace('class="mark" href="https://farax-creative.github.io/#zap-doctor"',
                  'class="mark" href="https://farax-creative.github.io/"')
    h = h.replace("https://farax-creative.github.io/#zap-doctor", PRODUCT_URL)
    h = h.replace("Back to Zap Doctor", "Back to Prompt Motion")
    h = h.replace("</head>", EXTRA_CSS + "</head>", 1)

    f = foot
    f = f.replace("https://farax-creative.github.io/#zap-doctor", PRODUCT_URL)
    f = f.replace("Back to Zap Doctor", "Back to Prompt Motion")
    f = f.replace("report/?product=Zap%20Doctor", "report/?product=Prompt%20Motion")
    f = re.sub(r"FARAX CREATIVE &middot; Zap series &middot; [^\n<]*",
               "FARAX CREATIVE &middot; Prompt Motion", f)
    # List this manual in the sidebar (only on this page; the Zap manuals
    # are built by their own scripts).
    f = f.replace('["zap-output", "Zap Output"]',
                  '["zap-output", "Zap Output"],\n    ["prompt-motion", "Prompt Motion"]')

    html = h + '<main class="wrap">\n' + CONTENT + "\n</main>\n\n" + f
    # The sidebar still lists the Zap manuals; nothing else may point at Doctor.
    body = html[:html.find("<!-- zt-sidebar:start -->")]
    assert "Zap Doctor" not in body and "#zap-doctor" not in body
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(html)
    print("wrote", os.path.normpath(OUT), len(html))


if __name__ == "__main__":
    build()
