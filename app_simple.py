import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Configure page
st.set_page_config(
    page_title="Malaria Analysis",
    layout="wide"
)

species_links = {
    "Plasmodium falciparum": "Plasmodium_falciparum:_Morphology",
    "Plasmodium vivax": "Plasmodium_vivax:_Morphology",
    "Plasmodium ovale": "Plasmodium_ovale:_Morphology",
    "Plasmodium malariae": "Plasmodium_malariae:_Morphology",
    "Plasmodium knowlesi": "Plasmodium_knowlesi:_Morphology",
}

def main():
    st.title("Malaria Cell Analysis")
    
    # Get API key from secrets
    try:
        api_key = st.secrets["gemini"]["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
    except Exception as e:
        st.error("API configuration error")
        return
    
    # File upload
    uploaded_file = st.file_uploader("Upload microscopy image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, width=400)
        
        # Analysis button
        if st.button("Analyze"):
            with st.spinner("Analyzing..."):
                try:
                    prompt = """
                    You are an expert in malaria parasite identification from blood smears. Analyze this Giemsa-stained thin blood film image for malaria parasites. First, determine if malaria parasites are present. If yes, identify the species based on the following detailed morphological characteristics:

                    ### Identifying Malaria Species from Blood Smears

                    The identification relies on microscopic features in Giemsa-stained thin blood films at slightly alkaline pH (around 7.4) for optimal visualization of dots and pigment. The five main human-infecting species are: Plasmodium falciparum, P. vivax, P. ovale, P. malariae, and P. knowlesi.

                    #### Plasmodium falciparum
                    - General: Causes severe malaria; small, delicate forms; multiple parasites per RBC; schizonts rare in peripheral blood; gametocytes distinctive.
                    - Rings/Early Trophozoites: Small, delicate rings; multiple per RBC; double chromatin dots; accolé (appliqué) forms; RBCs normal size, no stippling.
                    - Late Trophozoites: Thicker rings; Maurer's dots in RBC; pigment appears.
                    - Schizonts: Rare; 16+ merozoites untidily clustered; pigment clumped.
                    - Gametocytes: Banana-shaped; single chromatin with pigment.
                    - Key: High parasitemia, multiple rings, accolé forms, banana gametocytes; differentiate from P. knowlesi by lack of band forms.

                    #### Plasmodium vivax
                    - General: Relapsing malaria; large, robust parasites; all stages circulate; RBCs enlarged/distorted with Schüffner's dots.
                    - Rings/Early Trophozoites: Large rings, become irregular; Schüffner's dots; RBCs enlarge.
                    - Late Trophozoites: Amoeboid; prominent dots; pigment irregular.
                    - Schizonts: Large; 16-32 merozoites; dots in cytoplasm.
                    - Gametocytes: Large, fill RBC; pigment clumped.
                    - Key: Enlarged RBCs with Schüffner's dots; all stages present; larger schizonts than P. ovale.

                    #### Plasmodium ovale
                    - General: Similar to P. vivax but milder; trophozoites ring-like; RBCs moderately enlarged, ovoid/fimbriated with James' dots.
                    - Rings/Early Trophozoites: Large, robust rings; James' dots; RBCs ovoid.
                    - Late Trophozoites: Thickened rings, comet shapes; prominent dots.
                    - Schizonts: Up to 16 merozoites; dots in cytoplasm.
                    - Gametocytes: Fill RBC; pigment circumferential.
                    - Key: Ovoid/fimbriated RBCs, James' dots; smaller schizonts than P. vivax.

                    #### Plasmodium malariae
                    - General: Quartan malaria; low parasitemia; all stages circulate; small, neat parasites; RBCs small/round, no dots.
                    - Rings/Early Trophozoites: Small rings; RBCs normal/small.
                    - Late Trophozoites: Band forms; angular.
                    - Schizonts: Daisy head; 8-12 merozoites around central pigment.
                    - Gametocytes: Small, round; scattered pigment.
                    - Key: Low count, daisy schizonts, band forms; differentiate from P. knowlesi by neater forms.

                    #### Plasmodium knowlesi
                    - General: Zoonotic; resembles P. falciparum early, P. malariae late; high parasitemia possible; RBCs unaffected but may distort with sparse stippling.
                    - Rings/Early Trophozoites: Small rings; double dots; multiple per RBC; no stippling.
                    - Late Trophozoites: Band-like; Sinton/Mulligan's stippling.
                    - Schizonts: Up to 16 merozoites, grape-like; stippling.
                    - Gametocytes: Small, round; pigment overlies.
                    - Key: Early like falciparum, late like malariae but less neat; sparse stippling.

                    Additional notes: Look for malaria pigment (brown/gold); phagocytosed pigment in leukocytes. Consider synchronicity, mixed infections.

                    Output strictly in JSON format with these keys:
                    - "presence": "yes" or "no"
                    - "species": full name like "Plasmodium falciparum" or "unknown" if cannot identify
                    - "stage": list of observed stages (e.g., ["rings", "schizonts"])
                    - "parasitemia": "low", "medium", "high", or "unknown"
                    - "confidence": "low", "medium", "high"
                    - "rationale": brief clinical explanation of your assessment
                    """
                    
                    response = model.generate_content([prompt, image])
                    
                    if response.text:
                        text = response.text
                        # Clean up if wrapped in code block
                        if text.startswith("```json"):
                            text = text[7:].strip()
                        if text.endswith("```"):
                            text = text[:-3].strip()
                        
                        analysis = json.loads(text)
                        
                        st.subheader("Analysis Results")
                        st.write(f"**Presence of malaria parasites:** {analysis['presence']}")
                        st.write(f"**Identified species:** {analysis['species']}")
                        st.write(f"**Observed stages:** {', '.join(analysis['stage'])}")
                        st.write(f"**Parasitemia level:** {analysis['parasitemia']}")
                        st.write(f"**Confidence level:** {analysis['confidence']}")
                        st.write("**Rationale:**")
                        st.write(analysis['rationale'])
                        
                        if analysis['presence'] == "yes" and analysis['species'] in species_links:
                            title = species_links[analysis['species']]
                            link = f"https://haematologyetc.org/index.php?title={title}"
                            st.markdown(f"Learn more: [{analysis['species']} Morphology]({link})")
                    else:
                        st.error("No response received")
                        
                except json.JSONDecodeError:
                    st.error("Failed to parse analysis response. Raw output:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()